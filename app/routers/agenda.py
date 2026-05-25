from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from app.models.schemas import AgendaCreateRequest
from app.services.agenda_service import AgendaService


router = APIRouter(prefix="/api", tags=["agenda"])

def get_agenda_service():
    from main import chatbot_service
    return chatbot_service.agenda_service


@router.get("/agenda")
async def list_agenda(
    data: Optional[str] = Query(None, description="Filtrar por data (YYYY-MM-DD)"),
    agenda: AgendaService = Depends(get_agenda_service),
):
    return agenda.listar(data=data)


@router.post("/agenda", status_code=201)
async def create_agenda(
    body: AgendaCreateRequest,
    agenda: AgendaService = Depends(get_agenda_service),
):
    return agenda.criar(
        nome=body.nome,
        data=body.data,
        horario=body.horario,
        descricao=body.descricao or "",
    )


@router.patch("/agenda/{id}/concluir")
async def concluir_agenda(
    id: int,
    agenda: AgendaService = Depends(get_agenda_service),
):
    item = agenda.concluir(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Compromisso não encontrado")
    return item


@router.delete("/agenda/{id}", status_code=204)
async def delete_agenda(
    id: int,
    agenda: AgendaService = Depends(get_agenda_service),
):
    ok = agenda.deletar(id)
    if not ok:
        raise HTTPException(status_code=404, detail="Compromisso não encontrado")
