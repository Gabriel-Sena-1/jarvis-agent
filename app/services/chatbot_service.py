import os
from pathlib import Path
from datetime import datetime
from app.services.rag_manager import RAGManager
from app.services.agenda_service import AgendaService
from app.services.recall_service import RecallService
from app.services.chat_service import ChatService
from app.services.tool_caller import ToolCaller
from app.services.logs_service import LogsService
from typing import Optional

DOCUMENTS_FOLDER_PATH = Path(__file__).parent.parent.parent / "infrastructure" / "documents"

class ChatbotService:
    def __init__(self):
        self.documents_folder = DOCUMENTS_FOLDER_PATH
        self.documents_folder.mkdir(exist_ok=True)

        self.rag_manager = RAGManager.get_instance()
        self.agenda_service = AgendaService()
        self.recall_service = RecallService()
        self.chat_service = ChatService()
        self.logs_service = LogsService()
        self.tool_caller = ToolCaller(self.rag_manager, self.agenda_service, self.recall_service, self.logs_service)

    async def process_question(self, question: str, chat_id: Optional[int] = None) -> dict:
        try:
            if chat_id is not None:
                chat = self.chat_service.obter_chat(chat_id)
                if not chat:
                    title = question[:40] + ("..." if len(question) > 40 else "")
                    new_chat = self.chat_service.criar_chat(title)
                    chat_id = new_chat["id"]
            else:
                title = question[:40] + ("..." if len(question) > 40 else "")
                new_chat = self.chat_service.criar_chat(title)
                chat_id = new_chat["id"]

            self.chat_service.adicionar_interacao(chat_id, question, "user")
            
            chat_ctx = self.chat_service.listar_ultimas_10_interacoes(chat_id)
            result = await self.tool_caller.handle(question, chat_ctx)
            
            answer = result.get("answer", "")
            self.chat_service.adicionar_interacao(chat_id, answer, "assistant")
            
            result["chat_id"] = chat_id
            return result
        except Exception as e:
            return {"answer": f"Erro ao processar pergunta: {str(e)}", "chunks_usados": 0, "chat_id": chat_id}

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
            "message": f"Arquivo {file_name} salvo com sucesso ({chunks} chunks adicionados ao RAG)",
        }

    async def list_files(self) -> dict:
        items = []
        if self.documents_folder.exists():
            for file_path in self.documents_folder.iterdir():
                if file_path.is_file():
                    stat = file_path.stat()
                    items.append({
                        "filename": file_path.name,
                        "size": stat.st_size,
                        "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    })
        return {"total": len(items), "items": items}

    def get_rag_stats(self) -> dict:
        return self.rag_manager.get_stats()
