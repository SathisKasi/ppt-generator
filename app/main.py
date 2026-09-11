import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import download, presentation, upload
from app.config import get_settings
from app.presentation.template_catalog import list_templates

logging.basicConfig(level=logging.INFO)
settings = get_settings()
app = FastAPI(title=settings.app_name)
app.include_router(upload.router, prefix="/api")
app.include_router(presentation.router, prefix="/api")
app.include_router(download.router, prefix="/api")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name}


@app.get("/api/templates")
def templates():
    return {"templates": list_templates(settings)}


@app.get("/")
def home():
    from fastapi.responses import FileResponse

    return FileResponse(Path("app/static/index.html"))