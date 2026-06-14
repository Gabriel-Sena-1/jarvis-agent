import json
import re
import inspect
from app.services.agenda_tools import AgendaTools
from app.services.agenda_service import AgendaService
from app.services.recall_service import RecallService
from app.services.logs_service import LogsService

TOOL_CALLS = (
    "consultar_agenda",
    "listar_tarefas",
    "adicionar_tarefa",
    "concluir_tarefa",
    "buscar_material_rag",
    "priorizar_hoje",
    "montar_plano_estudos",
    "gerar_perguntas_recall",
    "avaliar_resposta_recall",
    "recomendar_revisao"
)

class ToolCaller:
    def __init__(self, rag_manager, agenda_service: AgendaService, recall_service: RecallService, logs_service: LogsService):
        self.rag_manager = rag_manager
        self.agenda = AgendaTools(agenda_service, recall_service, rag_manager)
        self.logs_service = logs_service

    def _prompt_classificar(self, question: str) -> str:
        return (
            "Você é um classificador de intenção. Analise a pergunta do usuário e responda "
            "APENAS com um JSON no formato exato abaixo, sem nenhum texto antes ou depois:\n\n"
            "{\n"
            '  "tipo": "consultar_agenda" | "listar_tarefas" | "adicionar_tarefa" | "concluir_tarefa" | '
            '"buscar_material_rag" | "priorizar_hoje" | "montar_plano_estudos" | "gerar_perguntas_recall" | "avaliar_resposta_recall" | '
            '"recomendar_revisao"\n'
            "}\n\n"
            "Diretrizes para classificação:\n"
            '- "consultar_agenda": Se o usuário quer saber o que tem na agenda, se tem algum compromisso, aula ou prova em algum dia/horário específico ou ver o calendário.\n'
            '- "listar_tarefas": Se o usuário quer listar todas as tarefas ou compromissos, ver tarefas pendentes ou concluídas de forma geral.\n'
            '- "adicionar_tarefa": Se o usuário quer adicionar, agendar, cadastrar ou marcar uma nova tarefa ou compromisso.\n'
            '- "concluir_tarefa": Se o usuário quer concluir, finalizar ou marcar como feito um compromisso ou tarefa.\n'
            '- "buscar_material_rag": Se o usuário faz perguntas informativas sobre os materiais/documentos de estudos, conceitos teóricos, explicações, resumos, ou qualquer dúvida conceitual.\n'
            '- "priorizar_hoje": Se o usuário pergunta o que deve priorizar HOJE, o que fazer agora, o que é mais urgente para hoje. Use este tipo quando a pergunta tem foco no DIA ATUAL e na prioridade imediata.\n'
            '- "montar_plano_estudos": Se o usuário quer montar um plano de estudos para vários dias, uma semana, ou organizar tempo de estudos de forma mais ampla. NÃO use para perguntas sobre o que priorizar hoje.\n'
            '- "gerar_perguntas_recall": Se o usuário quer gerar perguntas de estudo, active recall, simulação de prova ou treinar com o conteúdo do RAG.\n'
            '- "avaliar_resposta_recall": Se o usuário está respondendo a uma pergunta de recall anteriormente feita pelo sistema.\n'
            '- "recomendar_revisao": Se o usuário quer saber o que revisar, recomendações de estudo ou ver dificuldades com base em erros passados.\n\n'
            f"Pergunta: {question}"
        )

    def _classify(self, question: str) -> str:
        try:
            raw = self.rag_manager.get_response(self._prompt_classificar(question))
            print(f"🔎 Classificação bruta: {raw}")
            match = re.search(r'\{[^{}]*"tipo"[^{}]*\}', raw, re.DOTALL)
            if match:
                data = json.loads(match.group())
                tipo = data.get("tipo", "buscar_material_rag")
                if tipo in TOOL_CALLS:
                    return tipo
        except Exception as e:
            print(f"⚠️ Erro na classificação: {e}")
        return "buscar_material_rag"

async def _buscar_rag(
    self,
    question: str,
    chat_ctx: list = None
) -> dict:

    resposta, docs = await self.rag_manager.responder_rag(
        question,
        chat_ctx=chat_ctx,
        metodo="hibrido",
        k=8,
        alpha=0.45
    )

    qtd = len(docs)

    # qualidade baseada na recuperação
    if qtd >= 5:
        confianca = "alta"

    elif qtd >= 2:
        confianca = "media"

    else:
        confianca = "baixa"

    if confianca == "baixa":

        return {
            "answer": (
                "Não encontrei contexto suficiente "
                "nos materiais carregados para responder "
                "com confiança."
            ),
            "chunks_usados": qtd,
            "confianca": confianca
        }

    return {
        "answer": resposta,
        "chunks_usados": qtd,
        "confianca": confianca
    }

    async def handle(self, question: str, chat_ctx: list = None) -> dict:
        print(f"🔍 question={question!r}")

        tipo = self._classify(question)
        print(f"🏷️  Classificação automática: {tipo}")

        tool_function = self.map_tool_to_function(tipo, chat_ctx)
        tool_call = tool_function(question)
        result = await tool_call if inspect.isawaitable(tool_call) else tool_call
        print(f"✅ Resultado da ferramenta '{tipo}': {result}")
        if self.logs_service:
            self.logs_service.salvar_log(pergunta=question, resposta=str(result), tool=tipo)
        return result
        
    
    def map_tool_to_function(self, tool_name: str, chat_ctx: list = None) -> callable:
        if tool_name == "consultar_agenda":
            return lambda q: self.agenda.consultar(q)
        elif tool_name == "listar_tarefas":
            return lambda q: self.agenda.listar_tarefas(q)
        elif tool_name == "adicionar_tarefa":
            return lambda q: self.agenda.adicionar(q)
        elif tool_name == "concluir_tarefa":
            return lambda q: self.agenda.concluir(q)
        elif tool_name == "buscar_material_rag":
            return lambda q: self._buscar_rag(q, chat_ctx=chat_ctx)
        elif tool_name == "priorizar_hoje":
            return lambda q: self.agenda.priorizar_hoje(q)
        elif tool_name == "montar_plano_estudos":
            return lambda q: self.agenda.montar_plano_estudos(q)
        elif tool_name == "gerar_perguntas_recall":
            return lambda q: self.agenda.gerar_perguntas_recall(q)
        elif tool_name == "avaliar_resposta_recall":
            return lambda q: self.agenda.avaliar_resposta_recall(q)
        elif tool_name == "recomendar_revisao":
            return lambda q: self.agenda.recomendar_revisao(q)
        else:
            return lambda q: self._buscar_rag(q, chat_ctx=chat_ctx)
