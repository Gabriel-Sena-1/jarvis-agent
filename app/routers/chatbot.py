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
    result = await service.process_question(request.question, tool_call=request.tool_call)
    return result

