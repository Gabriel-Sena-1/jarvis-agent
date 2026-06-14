from fastapi import APIRouter, Depends
from app.models.schemas import AskRequest, AskResponse

router = APIRouter(prefix="/api", tags=["chatbot"])

# Função para obter a instância global do ChatbotService
def get_chatbot_service():
    from main import chatbot_service
    return chatbot_service


@router.post("/ask", response_model=AskResponse)
async def ask(
    request: AskRequest,
    service = Depends(get_chatbot_service)
):
    result = await service.process_question(request.question, chat_id=request.chat_id)
    return result


@router.get("/chats")
async def list_chats(service = Depends(get_chatbot_service)):
    return service.chat_service.listar_chats()


@router.get("/chats/{chat_id}/messages")
async def list_messages(chat_id: int, service = Depends(get_chatbot_service)):
    from fastapi import HTTPException
    chat = service.chat_service.obter_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat não encontrado")
    return service.chat_service.listar_interacoes(chat_id)


@router.delete("/chats/{chat_id}", status_code=204)
async def delete_chat(chat_id: int, service = Depends(get_chatbot_service)):
    from fastapi import HTTPException
    ok = service.chat_service.deletar_chat(chat_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Chat não encontrado")

