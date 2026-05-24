import os
import json
import re
from pathlib import Path
from datetime import datetime, date, timedelta
from app.services.rag_manager import RAGManager
from app.services.agenda_service import AgendaService

# Pasta onde os documentos são salvos e carregados para o RAG
DOCUMENTS_FOLDER_PATH = Path(__file__).parent.parent.parent / "infrastructure" / "documents"

def get_classify_prompt(question: str) -> str:
    return f"""\
Você é um classificador de intenção. Analise a pergunta do usuário e responda \
APENAS com um JSON no formato exato abaixo, sem nenhum texto antes ou depois:

{{"tipo": "agenda"}}   — se a pergunta for sobre compromissos, tarefas, aulas, provas, \
horários, agenda pessoal, o que tem hoje/amanhã/esta semana, eventos pendentes ou concluídos.

{{"tipo": "documentos"}}   — se a pergunta for sobre conteúdo de documentos, matérias, \
resumos, conceitos, explicações ou qualquer outro assunto que não seja agenda.

Pergunta: {question}
"""

class ChatbotService:
    def __init__(self):
        self.documents_folder = DOCUMENTS_FOLDER_PATH
        self.documents_folder.mkdir(exist_ok=True)

        self.rag_manager = RAGManager.get_instance()
        self.agenda_service = AgendaService()

    def _classify_question(self, question: str) -> str:
        """Retorna 'agenda' ou 'documentos' usando o LLM como classificador."""
        print(f"🔍 Classificando pergunta: {question}")
        try:
            prompt = get_classify_prompt(question)
            print(f"📋 Classificando intenção com prompt:\n{prompt}")
            raw = self.rag_manager.get_response(prompt)
            print(f"Resposta bruta da classificação: {raw}")
            # extrai o primeiro JSON da resposta
            match = re.search(r'\{[^{}]*"tipo"[^{}]*\}', raw, re.DOTALL)
            if match:
                data = json.loads(match.group())
                tipo = data.get("tipo", "documentos")
                if tipo in ("agenda", "documentos"):
                    return tipo
        except Exception as e:
            print(f"⚠️ Erro na classificação: {e}")
        return "documentos"

    def _build_agenda_context(self, question: str) -> str:
        """Monta um bloco de texto com os compromissos relevantes para a pergunta."""
        q = question.lower()
        today = date.today()

        if "hoje" in q:
            items = self.agenda_service.listar(data=today.isoformat())
            label = f"hoje ({today.isoformat()})"
        elif "amanhã" in q or "amanha" in q:
            tomorrow = today + timedelta(days=1)
            items = self.agenda_service.listar(data=tomorrow.isoformat())
            label = f"amanhã ({tomorrow.isoformat()})"
        elif "semana" in q:
            # próximos 7 dias
            all_items = self.agenda_service.listar()
            end = today + timedelta(days=7)
            items = [
                i for i in all_items
                if today.isoformat() <= i["data"] <= end.isoformat()
            ]
            label = f"esta semana ({today.isoformat()} a {end.isoformat()})"
        else:
            items = self.agenda_service.listar()
            label = "todos os compromissos"

        if not items:
            return f"Não há compromissos agendados para {label}."

        linhas = [f"Compromissos ({label}):"]
        for it in items:
            status = "✅ concluído" if it.get("finished_at") else "⏳ pendente"
            desc = f" — {it['descricao']}" if it.get("descricao") else ""
            linhas.append(f"- [{status}] {it['nome']} em {it['data']} às {it['horario']}{desc}")
        return "\n".join(linhas)
    
    async def warmup(self):
        if not self.documents_folder.exists():
            return
        
        for file_path in self.documents_folder.iterdir():
            if file_path.is_file():
                try:
                    if file_path.suffix.lower() in ['.txt', '.pdf']:
                        chunks = self.rag_manager.carregar_documento_arquivo(str(file_path))
                        print(f"✓ Carregado {file_path.name}: {chunks} chunks")
                except Exception as e:
                    print(f"✗ Erro ao carregar {file_path.name}: {str(e)}")
    
    async def process_question(self, question: str) -> dict:
        """
        Processa uma pergunta usando RAG + contexto de agenda quando relevante.
        A classificação da intenção é feita pelo próprio LLM.
        """
        try:
            print(f"🔍 Processando pergunta: {question}")

            # Classifica a intenção via LLM
            tipo = self._classify_question(question)
            print(f"🏷️  Classificação: {tipo}")

            agenda_context = ""
            if tipo == "agenda":
                agenda_context = "\n\n" + self._build_agenda_context(question)
                print("📅 Contexto de agenda injetado")

            resposta, docs = await self.rag_manager.responder_rag(
                question,
                metodo="hibrido",
                k=10,
                extra_context=agenda_context,
            )
            return {
                "answer": resposta,
                "chunks_usados": len(docs)
            }
        except Exception as e:
            return {
                "answer": f"Erro ao processar pergunta: {str(e)}",
                "chunks_usados": 0
            }
    
    async def save_uploaded_file(self, file_name: str, file_content: bytes) -> dict:
        file_path = self.documents_folder / file_name
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        file_size = os.path.getsize(file_path)
        
        try:
            chunks = self.rag_manager.carregar_documento_arquivo(str(file_path))
        except Exception as e:
            chunks = 0
            print(f"Aviso: Não foi possível processar {file_name} no RAG: {str(e)}")
        
        return {
            "filename": file_name,
            "size": file_size,
            "message": f"Arquivo {file_name} salvo com sucesso ({chunks} chunks adicionados ao RAG)"
        }
    
    async def list_files(self) -> dict:
        items = []
        
        if self.documents_folder.exists():
            for file_path in self.documents_folder.iterdir():
                if file_path.is_file():
                    file_stat = file_path.stat()
                    items.append({
                        "filename": file_path.name,
                        "size": file_stat.st_size,
                        "created_at": datetime.fromtimestamp(file_stat.st_ctime).isoformat()
                    })
        
        return {
            "total": len(items),
            "items": items
        }
    
    def get_rag_stats(self) -> dict:
        return self.rag_manager.get_stats()
