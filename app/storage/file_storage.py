import json
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.config import Settings


class FileStorage:
    def __init__(self, settings: Settings):
        self.settings = settings

    def new_id(self) -> str:
        return uuid.uuid4().hex

    def upload_path(self, file_id: str, suffix: str) -> Path:
        return self.settings.upload_directory / f"{file_id}{suffix.lower()}"

    async def save_upload(self, upload: UploadFile, file_id: str) -> tuple[Path, int]:
        suffix = Path(upload.filename or "").suffix
        destination = self.upload_path(file_id, suffix)
        size = 0
        with destination.open("wb") as target:
            while chunk := await upload.read(1024 * 1024):
                size += len(chunk)
                if size > self.settings.max_upload_size_mb * 1024 * 1024:
                    destination.unlink(missing_ok=True)
                    raise ValueError("File exceeds the configured upload size limit.")
                target.write(chunk)
        return destination, size

    def output_path(self, file_id: str) -> Path:
        return self.settings.output_directory / f"{file_id}-presentation.pptx"

    def write_status(self, file_id: str, status: dict) -> None:
        (self.settings.output_directory / f"{file_id}.json").write_text(
            json.dumps(status, indent=2), encoding="utf-8"
        )

    def read_status(self, file_id: str) -> dict:
        status_path = self.settings.output_directory / f"{file_id}.json"
        if not status_path.exists():
            raise FileNotFoundError(file_id)
        return json.loads(status_path.read_text(encoding="utf-8"))