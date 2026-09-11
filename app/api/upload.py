from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import get_settings
from app.processors import supported_extensions
from app.storage.file_storage import FileStorage

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    settings = get_settings()
    original_name = file.filename or "upload"
    suffix = Path(original_name).suffix.lower()
    if suffix not in supported_extensions():
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {suffix or 'unknown'}. Allowed formats: PDF, DOCX, PPTX, XLSX, CSV, TXT, Markdown.",
        )
    storage = FileStorage(settings)
    file_id = storage.new_id()
    try:
        path, size = await storage.save_upload(file, file_id)
    except ValueError as error:
        raise HTTPException(status_code=413, detail=str(error)) from error
    status = {"file_id": file_id, "file_name": original_name, "file_type": suffix[1:], "file_size": size, "status": "uploaded", "input_path": str(path)}
    storage.write_status(file_id, status)
    return status