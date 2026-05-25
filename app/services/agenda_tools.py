"""
Ferramentas de agenda: prompts, geração de insumos e execução das tools.
Cada método segue o fluxo: gera insumo → cria prompt → chama IA → retorna dict.
"""

import json
import re
from datetime import date
from app.services.agenda_service import AgendaService


class AgendaTools:
    def __init__(self, agenda_service: AgendaService, rag_manager):
        self.agenda_service = agenda_service
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

    def _prompt_responder(self, question: str, ctx: str) -> str:
        return (
            "Você é o Jarvis, assistente pessoal. Responda em português com base nos compromissos abaixo.\n"
            "Se não houver informação suficiente, diga isso claramente.\n\n"
            f"{ctx}\n\n"
            f"Dia atual: {date.today().isoformat()}\n\n"
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

    def consultar(self, question: str) -> dict:
        ctx = self._build_context()
        prompt = self._prompt_responder(question, ctx)
        resposta = self.rag_manager.get_response(prompt)
        return {"answer": resposta, "chunks_usados": 0}

    def listar_tarefas(self, question: str) -> dict:
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
        prompt = self._prompt_responder(question, ctx)
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
