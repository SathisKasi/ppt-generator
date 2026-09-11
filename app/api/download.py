from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import get_settings
from app.storage.file_storage import FileStorage

router = APIRouter()


@router.get("/download/{file_id}")
def download(file_id: str):
    try:
        status = FileStorage(get_settings()).read_status(file_id)
        output_path = Path(status.get("output_path", ""))
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail="Presentation not found.") from error
    if status.get("status") != "generated" or not output_path.is_file():
        raise HTTPException(status_code=404, detail="Presentation has not been generated yet.")
    return FileResponse(output_path, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation", filename=f"{file_id}-presentation.pptx")