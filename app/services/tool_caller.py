import json
import re
from app.services.agenda_tools import AgendaTools
from app.services.agenda_service import AgendaService

TOOL_CALLS = ("consultar_agenda", "listar_tarefas", "adicionar_tarefa", "concluir_tarefa", "buscar_material_rag")

class ToolCaller:
    def __init__(self, rag_manager, agenda_service: AgendaService):
        self.rag_manager = rag_manager
        self.agenda = AgendaTools(agenda_service, rag_manager)

    def _prompt_classificar(self, question: str) -> str:
        return (
            "Você é um classificador de intenção. Analise a pergunta do usuário e responda "
            "APENAS com um JSON no formato exato abaixo, sem nenhum texto antes ou depois:\n\n"
            '{"tipo": "agenda"}   — se a pergunta for sobre compromissos, tarefas, aulas, provas, '
            "horários, agenda pessoal, o que tem hoje/amanhã/esta semana, eventos pendentes ou concluídos.\n\n"
            '{"tipo": "documentos"}   — se a pergunta for sobre conteúdo de documentos, matérias, '
            "resumos, conceitos, explicações ou qualquer outro assunto que não seja agenda.\n\n"
            f"Pergunta: {question}"
        )

    def _classify(self, question: str) -> str:
        try:
            raw = self.rag_manager.get_response(self._prompt_classificar(question))
            print(f"🔎 Classificação bruta: {raw}")
            match = re.search(r'\{[^{}]*"tipo"[^{}]*\}', raw, re.DOTALL)
            if match:
                data = json.loads(match.group())
                tipo = data.get("tipo", "documentos")
                if tipo in ("agenda", "documentos"):
                    return tipo
        except Exception as e:
            print(f"⚠️ Erro na classificação: {e}")
        return "documentos"


    async def _buscar_rag(self, question: str) -> dict:
        resposta, docs = await self.rag_manager.responder_rag(question, metodo="hibrido", k=10)
        return {"answer": resposta, "chunks_usados": len(docs)}

    async def handle(self, question: str, tool_call: str | None) -> dict:
        print(f"🔍 tool_call={tool_call!r} | question={question!r}")

        if tool_call == "consultar_agenda":
            return self.agenda.consultar(question)

        if tool_call == "listar_tarefas":
            return self.agenda.listar_tarefas(question)

        if tool_call == "adicionar_tarefa":
            return self.agenda.adicionar(question)

        if tool_call == "concluir_tarefa":
            return self.agenda.concluir(question)

        if tool_call == "buscar_material_rag":
            return await self._buscar_rag(question)

        tipo = self._classify(question)
        print(f"🏷️  Classificação automática: {tipo}")
        if tipo == "agenda":
            return self.agenda.consultar(question)
        return await self._buscar_rag(question)
