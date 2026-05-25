from pydantic import BaseModel
from typing import Optional


class AskRequest(BaseModel):
    question: str
    tool_call: Optional[str] = None


class AskResponse(BaseModel):
    answer: str
    chunks_usados: Optional[int] = None


class FileUploadResponse(BaseModel):
    filename: str
    size: int
    message: str


class FileInfo(BaseModel):
    filename: str
    size: int
    created_at: str


class FileListResponse(BaseModel):
    total: int
    items: list[FileInfo]


class AgendaCreateRequest(BaseModel):
    nome: str
    data: str
    horario: str
    descricao: Optional[str] = ""
