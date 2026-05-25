from fastapi import APIRouter, UploadFile, File, Depends
from app.models.schemas import FileUploadResponse, FileListResponse

router = APIRouter(prefix="/api", tags=["files"])

def get_chatbot_service():
    from main import chatbot_service
    return chatbot_service


@router.post("/files/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    service = Depends(get_chatbot_service)
):
    content = await file.read()
    result = await service.save_uploaded_file(file.filename, content)
    return result


@router.get("/files", response_model=FileListResponse)
async def list_files(service = Depends(get_chatbot_service)):
    result = await service.list_files()
    return result

