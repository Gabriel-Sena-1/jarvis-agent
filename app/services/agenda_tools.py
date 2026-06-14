"""
Ferramentas de agenda: prompts, geração de insumos e execução das tools.
Cada método segue o fluxo: gera insumo → cria prompt → chama IA → retorna dict.
"""

import json
import re
from datetime import date
from app.services.agenda_service import AgendaService
from app.services.recall_service import RecallService


class AgendaTools:
    def __init__(self, agenda_service: AgendaService, recall_service: RecallService, rag_manager):
        self.agenda_service = agenda_service
        self.recall_service = recall_service
        self.rag_manager = rag_manager

    # ── insumos ────────────────────────────────────────────────────────────────

    def _build_context(self, items: list | None = None) -> str:
        """Gera o bloco de texto com os compromissos para injetar no prompt."""
        if items is None:
            items = self.agenda_service.listar()
        linhas = ["Compromissos:"]
        for it in items:
            status = "Concluído" if it.get("finished_at") else "Pendente"
            linhas.append(
                f"- [id:{it['id']}] {it['nome']} em {it['data']} às {it['horario']} (Status: {status})"
            )
        return "\n".join(linhas)

    def _extract_json(self, raw: str) -> dict | None:
        match = re.search(r'\{[^{}]*\}', raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                return None
        return None

    # ── prompts ────────────────────────────────────────────────────────────────

    def _prompt_responder(self, question: str, ctx: str, chat_ctx: str) -> str:
        return (
            "Você é o Jarvis, assistente pessoal. Responda em português com base nos compromissos abaixo.\n"
            "Se não houver informação suficiente, diga isso claramente.\n\n"
            f"{ctx}\n\n"
            f"Dia atual: {date.today().isoformat()}\n\n"
            f"Contexto do chat: {chat_ctx}\n\n"
            f"Pergunta: {question}"
        )

    def _prompt_adicionar(self, question: str) -> str:
        return (
            f"Dia atual: {date.today().isoformat()}\n\n"
            "Você é um assistente que extrai dados de compromissos a partir da mensagem do usuário.\n"
            "Responda APENAS com um JSON no formato exato abaixo, sem nenhum texto antes ou depois:\n\n"
            '{"nome": "...", "data": "YYYY-MM-DD", "horario": "HH:MM", "descricao": "..."}\n\n'
            'O campo "descricao" é opcional (pode ser string vazia).\n'
            "Se não for possível extrair nome, data ou horário, responda:\n"
            '{"erro": "motivo da falha"}\n\n'
            f"Mensagem do usuário: {question}"
        )

    def _prompt_concluir(self, question: str, ctx: str) -> str:
        return (
            "Você é um assistente que identifica qual compromisso o usuário quer concluir.\n"
            "Com base na lista abaixo e na pergunta do usuário, responda APENAS com um JSON:\n\n"
            '{"id": <numero inteiro>}\n\n'
            "Se não for possível identificar, responda:\n"
            '{"erro": "motivo"}\n\n'
            f"{ctx}\n\n"
            f"Pergunta: {question}"
        )

    # ── tools ──────────────────────────────────────────────────────────────────

    async def consultar(self, question: str, chat_ctx: str) -> dict:
        ctx = self._build_context()
        prompt = self._prompt_responder(question, ctx, chat_ctx)
        resposta = self.rag_manager.get_response(prompt)
        return {"answer": resposta, "chunks_usados": 0}

    async def listar_tarefas(self, question: str, chat_ctx: str) -> dict:
        all_items = self.agenda_service.listar()
        q = question.lower()

        if "pendente" in q or "pendentes" in q:
            items = [i for i in all_items if not i.get("finished_at")]
            label = "Tarefas pendentes"
        elif "concluíd" in q or "concluid" in q or "feito" in q or "feitas" in q:
            items = [i for i in all_items if i.get("finished_at")]
            label = "Tarefas concluídas"
        else:
            items = all_items
            label = "Todas as tarefas"

        ctx = label + ":\n" + "\n".join(
            f"- [id:{it['id']}] {it['nome']} em {it['data']} às {it['horario']} "
            f"(Status: {'Concluído' if it.get('finished_at') else 'Pendente'})"
            for it in items
        )
        prompt = self._prompt_responder(question, ctx, chat_ctx)
        resposta = self.rag_manager.get_response(prompt)
        return {"answer": resposta, "chunks_usados": 0}

    def adicionar(self, question: str) -> dict:
        prompt = self._prompt_adicionar(question)
        raw = self.rag_manager.get_response(prompt)
        print(f"📦 Payload gerado pela IA: {raw}")

        data = self._extract_json(raw)

        if data is None:
            return {"answer": "Não consegui entender os dados do compromisso. Por favor, informe nome, data e horário.", "chunks_usados": 0}

        if "erro" in data:
            return {"answer": f"Não foi possível criar o compromisso: {data['erro']}", "chunks_usados": 0}

        ausentes = [c for c in ("nome", "data", "horario") if not data.get(c)]
        if ausentes:
            return {"answer": f"Faltam as seguintes informações: {', '.join(ausentes)}.", "chunks_usados": 0}

        criado = self.agenda_service.criar(
            nome=data["nome"],
            data=data["data"],
            horario=data["horario"],
            descricao=data.get("descricao", ""),
        )
        resposta = (
            f"Compromisso criado com sucesso!\n"
            f"- Nome: {criado['nome']}\n"
            f"- Data: {criado['data']}\n"
            f"- Horário: {criado['horario']}\n"
            + (f"- Descrição: {criado['descricao']}" if criado.get("descricao") else "")
        )
        return {"answer": resposta, "chunks_usados": 0}

    def concluir(self, question: str) -> dict:
        ctx = self._build_context()
        prompt = self._prompt_concluir(question, ctx)
        raw = self.rag_manager.get_response(prompt)
        print(f"🔑 ID identificado pela IA: {raw}")

        data = self._extract_json(raw)

        if data is None or "erro" in (data or {}):
            motivo = data.get("erro", "não identificado") if data else "não identificado"
            return {"answer": f"Não consegui identificar o compromisso a concluir: {motivo}", "chunks_usados": 0}

        id_tarefa = data.get("id")
        if not isinstance(id_tarefa, int):
            return {"answer": "Não foi possível identificar o ID do compromisso. Por favor, seja mais específico.", "chunks_usados": 0}

        concluido = self.agenda_service.concluir(id_tarefa)
        if concluido is None:
            return {"answer": f"Compromisso com id {id_tarefa} não encontrado.", "chunks_usados": 0}

        return {"answer": f"Compromisso '{concluido['nome']}' marcado como concluído com sucesso!", "chunks_usados": 0}

    # ── Novas Ferramentas T2 ──────────────────────────────────────────────────

    async def priorizar_hoje(self, question: str) -> dict:
        compromissos = self.agenda_service.listar()
        ctx_agenda = self._build_context(compromissos) if compromissos else "Nenhum compromisso cadastrado na agenda."

        docs = []
        if self.rag_manager.chunks:
            docs = self.rag_manager.recuperar_hibrido(question, k=5)

        ctx_docs = self.rag_manager.build_doc_context(docs) if docs else "Nenhum material de estudo carregado."

        prompt = self._prompt_priorizar_hoje(question, ctx_agenda, ctx_docs)
        resposta = self.rag_manager.get_response(prompt)
        return {"answer": resposta, "chunks_usados": len(docs)}

    async def montar_plano_estudos(self, question: str) -> dict:
        compromissos = self.agenda_service.listar()
        ctx_agenda = self._build_context(compromissos) if compromissos else "Nenhum compromisso cadastrado na agenda."

        docs = []
        if self.rag_manager.chunks:
            docs = self.rag_manager.recuperar_hibrido(question, k=8)

        ctx_docs = self.rag_manager.build_doc_context(docs)

        if not docs:
            return {
                "answer": "Não há material carregado para planejar os estudos. Por favor, faça upload de arquivos PDF/TXT para continuar.",
                "chunks_usados": 0
            }

        prompt = self._prompt_plano_estudos(question, ctx_agenda, ctx_docs)
        resposta = self.rag_manager.get_response(prompt)
        return {"answer": resposta, "chunks_usados": len(docs)}

    def _topico_presente_nos_docs(self, topico: str, docs: list[dict]) -> bool:
        """Verifica se as palavras-chave do tópico aparecem em pelo menos um chunk recuperado."""
        palavras = [p.strip().lower() for p in topico.replace(",", " ").split() if len(p.strip()) > 3]
        if not palavras:
            return True  # sem palavras-chave suficientes para filtrar
        texto_total = " ".join(d.get("texto", "").lower() for d in docs)
        matches = sum(1 for p in palavras if p in texto_total)
        # considera relevante se ao menos 40% das palavras-chave do tópico aparecem
        return matches >= max(1, len(palavras) * 0.4)

    def _extrair_topico(self, question: str) -> str:
        """Extrai o tema principal da pergunta (após 'sobre', 'de', etc.)."""
        q = question.lower()
        for prep in ["sobre ", "de ", "acerca de ", "referente a ", "em "]:
            if prep in q:
                return question[q.index(prep) + len(prep):].strip()
        return question.strip()

    async def gerar_perguntas_recall(self, question: str) -> dict:
        if not self.rag_manager.chunks:
            return {
                "answer": "Não há material carregado para treinar com Active Recall. Faça upload de arquivos PDF/TXT para continuar.",
                "chunks_usados": 0
            }

        topico = self._extrair_topico(question)
        docs = self.rag_manager.recuperar_hibrido(question, k=8)
        if not docs:
            return {
                "answer": f"Não encontrei material sobre **{topico}** nos documentos carregados. Faça upload do documento correspondente para continuar.",
                "chunks_usados": 0
            }

        # Guard anti-alucinação: verifica se os docs recuperados são realmente sobre o tópico pedido
        if not self._topico_presente_nos_docs(topico, docs):
            print(f"⚠️ Chunks recuperados não contêm o tópico '{topico}'. Abortando recall.")
            return {
                "answer": (
                    f"Não encontrei conteúdo sobre **{topico}** nos documentos carregados.\n"
                    "Para treinar com Active Recall sobre este tema, faça upload do material correspondente."
                ),
                "chunks_usados": 0
            }

        ctx_docs = self.rag_manager.build_doc_context(docs)
        prompt = self._prompt_gerar_perguntas(question, ctx_docs, topico=topico)
        raw = self.rag_manager.get_response(prompt)

        perguntas = self._extract_recall_json(raw) or []

        if len(perguntas) < 5 and len(self.rag_manager.chunks) > 8:
            print(f"⚠️ Apenas {len(perguntas)} perguntas geradas. Buscando mais chunks...")
            docs_extendidos = self.rag_manager.recuperar_hibrido(question, k=16)
            novos_docs = [d for d in docs_extendidos if d not in docs]
            if novos_docs and self._topico_presente_nos_docs(topico, novos_docs):
                docs = docs + novos_docs
                ctx_docs = self.rag_manager.build_doc_context(docs)
                prompt = self._prompt_gerar_perguntas(question, ctx_docs, topico=topico)
                raw = self.rag_manager.get_response(prompt)
                perguntas_novas = self._extract_recall_json(raw) or []
                for p in perguntas_novas:
                    if len(perguntas) >= 5:
                        break
                    if not any(ep["pergunta"] == p["pergunta"] for ep in perguntas):
                        p["id"] = len(perguntas) + 1
                        perguntas.append(p)

        if not perguntas:
            return {
                "answer": "Não consegui gerar perguntas com base no material encontrado. Tente reformular a pergunta.",
                "chunks_usados": len(docs)
            }

        doc_nomes = list(set([d.get("documento", "documento") for d in docs]))
        doc_nome = doc_nomes[0] if doc_nomes else "documento"

        for p in perguntas:
            self.recall_service.salvar_pergunta_recall(
                documento=doc_nome,
                pergunta=p["pergunta"],
                resposta_correta=p["resposta_esperada"]
            )

        linhas_perguntas = []
        for i, p in enumerate(perguntas):
            linhas_perguntas.append(f"**Pergunta {i+1}**: {p['pergunta']}")

        resposta_final = (
            f"Aqui estão {len(perguntas)} perguntas de **Active Recall** sobre **{topico}**:\n\n"
            + "\n\n".join(linhas_perguntas)
            + "\n\n---\n"
            "💬 **Responda a Pergunta 1 no chat agora!** Digite sua resposta e eu avalio para você."
        )

        return {"answer": resposta_final, "chunks_usados": len(docs)}

    def avaliar_resposta_recall(self, question: str) -> dict:
        pendente = self.recall_service.obter_recall_pendente()
        if not pendente:
            return {
                "answer": "Não encontrei nenhuma pergunta de Active Recall pendente de resposta. Inicie um novo treino com `/gerar_perguntas_recall`.",
                "chunks_usados": 0
            }

        prompt = self._prompt_avaliar_resposta(
            pergunta=pendente["pergunta"],
            gabarito=pendente["resposta_correta"],
            resposta_usuario=question
        )

        raw_eval = self.rag_manager.get_response(prompt)
        print(f"📦 Avaliação da resposta: {raw_eval}")

        eval_data = self._extract_json(raw_eval)

        avaliacao = "incorreta"
        feedback = "Não foi possível extrair a avaliação do LLM."

        if eval_data:
            avaliacao = eval_data.get("avaliacao", "incorreta").lower()
            if avaliacao not in ("correta", "parcial", "incorreta"):
                avaliacao = "incorreta"
            feedback = eval_data.get("feedback", "")

        self.recall_service.atualizar_resposta_recall(
            id=pendente["id"],
            resposta_usuario=question,
            avaliacao=avaliacao
        )

        ultimas = self.recall_service.obter_ultimas_perguntas(limite=5)
        concluidas = [u for u in ultimas if u["resposta_usuario"] is not None]
        proximo_pendente = self.recall_service.obter_recall_pendente()

        resultado = (
            f"### Avaliação da sua resposta:\n"
            f"- **Avaliação**: {avaliacao.upper()}\n"
            f"- **Feedback**: {feedback}\n\n"
        )

        if len(concluidas) == 5:
            corretas = sum(1 for u in ultimas if u["avaliacao"] == "correta")
            parciais = sum(1 for u in ultimas if u["avaliacao"] == "parcial")
            score = corretas + (parciais * 0.5)

            reforcar = [u["pergunta"] for u in ultimas if u["avaliacao"] != "correta"]
            lista_reforco = "\n".join([f"- {r}" for r in reforcar]) if reforcar else "Nenhum! Excelente desempenho!"

            resultado += (
                f"🎉 **Sessão de Active Recall concluída!**\n"
                f"- **Resultado final**: {corretas} corretas, {parciais} parciais de 5 perguntas (Score: {score}/5.0)\n"
                f"- **Tópicos para reforçar**:\n{lista_reforco}\n"
            )
        elif proximo_pendente:
            resultado += f"**Próxima pergunta**: {proximo_pendente['pergunta']}"
        else:
            totais = len(concluidas)
            corretas = sum(1 for u in ultimas if u["resposta_usuario"] is not None and u["avaliacao"] == "correta")
            parciais = sum(1 for u in ultimas if u["resposta_usuario"] is not None and u["avaliacao"] == "parcial")
            score = corretas + (parciais * 0.5)
            reforcar = [u["pergunta"] for u in ultimas if u["resposta_usuario"] is not None and u["avaliacao"] != "correta"]
            lista_reforco = "\n".join([f"- {r}" for r in reforcar]) if reforcar else "Nenhum!"

            resultado += (
                f"🎉 **Sessão de Active Recall concluída!**\n"
                f"- **Resultado final**: {corretas} corretas, {parciais} parciais de {totais} perguntas (Score: {score}/{totais}.0)\n"
                f"- **Tópicos para reforçar**:\n{lista_reforco}\n"
            )

        return {"answer": resultado, "chunks_usados": 0}

    def recomendar_revisao(self, question: str) -> dict:
        historico = self.recall_service.listar_recall_com_erros()
        if not historico:
            return {
                "answer": "Nenhum histórico de treino encontrado ainda. Faça ao menos uma sessão de Active Recall primeiro!",
                "chunks_usados": 0
            }

        erros_por_doc = {}
        for item in historico:
            doc = item["documento"]
            erros_por_doc[doc] = erros_por_doc.get(doc, {"erros": 0, "total": 0})
            erros_por_doc[doc]["total"] += 1
            if item["avaliacao"] != "correta":
                erros_por_doc[doc]["erros"] += 1

        ctx = json.dumps(erros_por_doc, ensure_ascii=False, indent=2)
        prompt = self._prompt_recomendar_revisao(ctx)
        resposta = self.rag_manager.get_response(prompt)
        return {"answer": resposta, "chunks_usados": 0}

    # ── Prompts e Helpers ─────────────────────────────────────────────────────

    def _prompt_priorizar_hoje(self, question: str, ctx_agenda: str, ctx_docs: str) -> str:
        return (
            "Você é o Jarvis, assistente de estudos e produtividade.\n"
            "O usuário quer saber o que deve PRIORIZAR HOJE. Responda de forma objetiva e direta, listando no máximo 3 itens de alta prioridade para hoje.\n"
            "Diretrizes OBRIGATÓRIAS:\n"
            f"- A data de HOJE é {date.today().isoformat()}. Use apenas esta data para avaliar prioridade.\n"
            "- Priorize compromissos com prazo HOJE ou AMANHÃ (provas, entregas, compromissos da agenda).\n"
            "- Se não houver provas ou entregas urgentes, indique os tópicos de estudo mais atrasados com base nos materiais.\n"
            "- NÃO gere um plano de vários dias. Foque SOMENTE no que é mais urgente PARA HOJE.\n"
            "- Seja objetivo e conciso. Máximo de 3 prioridades numeradas.\n\n"
            f"AGENDA:\n{ctx_agenda}\n\n"
            f"MATERIAIS DISPONÍVEIS (para identificar tópicos relevantes):\n{ctx_docs}\n\n"
            f"Pergunta do usuário: {question}"
        )

    def _prompt_plano_estudos(self, question: str, ctx_agenda: str, ctx_docs: str) -> str:
        return (
            "Você é o Jarvis, assistente de estudos. "
            "Monte um plano de estudos detalhado em português com base nas informações fornecidas abaixo.\n"
            "Diretrizes:\n"
            "- Liste os tópicos por dia, estimativa de tempo e qual material (documento/trecho) consultar.\n"
            "- Cite explicitamente quais materiais (documentos) foram usados no plano.\n"
            "- Se a agenda estiver vazia (ou sem compromissos relevantes), avise explicitamente e gere um plano genérico com base nos materiais disponíveis.\n"
            "- Se faltar algum compromisso relevante, informe de maneira clara.\n"
            f"- A data atual é {date.today().isoformat()}. Somente mencione datas reais a partir desta.\n\n"
            f"AGENDA:\n{ctx_agenda}\n\n"
            f"MATERIAIS DISPONÍVEIS:\n{ctx_docs}\n\n"
            f"Solicitação do usuário: {question}"
        )

    def _prompt_gerar_perguntas(self, question: str, ctx_docs: str, topico: str = "") -> str:
        topico_instrucao = (
            f"ATENÇÃO: As perguntas devem ser EXCLUSIVAMENTE sobre o tema '{topico}'. "
            f"Não gere perguntas sobre outros assuntos que não sejam '{topico}'.\n"
            if topico else ""
        )
        return (
            "Você é o Jarvis, assistente de estudos especializado em Active Recall.\n"
            f"{topico_instrucao}"
            "Com base nos trechos de documentos fornecidos abaixo, gere exatamente 5 perguntas de Active Recall "
            "desafiadoras sobre o conteúdo, juntamente com suas respostas esperadas (gabarito).\n"
            "REGRAS OBRIGATÓRIAS:\n"
            "- Use APENAS informações presentes nos trechos fornecidos. NÃO invente conteúdo.\n"
            "- As perguntas devem testar compreensão profunda, não decoreba.\n"
            "Responda APENAS com um JSON válido (um array de objetos), sem blocos de texto antes ou depois.\n"
            "O formato do JSON deve ser exatamente:\n"
            '[{"id": 1, "pergunta": "...", "resposta_esperada": "..."}, ...]\n\n'
            f"MATERIAL DISPONÍVEL:\n{ctx_docs}\n\n"
            f"Solicitação do usuário: {question}"
        )

    def _prompt_avaliar_resposta(self, pergunta: str, gabarito: str, resposta_usuario: str) -> str:
        return (
            "Você é o Jarvis, assistente de estudos. Avalie a resposta do aluno para a pergunta fornecida abaixo com base no gabarito oficial.\n"
            "Responda APENAS com um JSON válido, sem blocos de texto explicativos antes ou depois. "
            "O formato do JSON deve ser exatamente:\n"
            '{"avaliacao": "correta"|"parcial"|"incorreta", "feedback": "uma explicação breve justificando a nota"}\n\n'
            f"Pergunta: {pergunta}\n"
            f"Gabarito: {gabarito}\n"
            f"Resposta do aluno: {resposta_usuario}"
        )

    def _prompt_recomendar_revisao(self, ctx_erros: str) -> str:
        return (
            "Você é o Jarvis, assistente de estudos. Analise os dados estatísticos abaixo que representam o "
            "histórico de erros e acertos do usuário nas sessões de estudo de Active Recall por documento/tema.\n"
            "Gere uma recomendação de revisão personalizada e motivadora em português. Diga quais assuntos ou documentos ele "
            "deve priorizar (onde há maior taxa de erro), sugerindo estratégias de estudo para superar essas dificuldades.\n\n"
            f"DADOS DE DESEMPENHO (JSON):\n{ctx_erros}"
        )

    def _extract_recall_json(self, raw: str) -> list | None:
        match = re.search(r'\[\s*\{.*\}\s*\]', raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        clean = raw.strip()
        if clean.startswith("```json"):
            clean = clean.split("```json")[1].split("```")[0].strip()
        elif clean.startswith("```"):
            clean = clean.split("```")[1].split("```")[0].strip()
        try:
            val = json.loads(clean)
            if isinstance(val, list):
                return val
        except Exception:
            pass
        return None
