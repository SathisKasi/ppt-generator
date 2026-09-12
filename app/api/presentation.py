import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from app.agents.document_agent import analyze
from app.agents.presentation_planner import plan, plan_with_llm
from app.agents.quality_agent import review
from app.config import get_settings
from app.presentation.ppt_generator import generate_pptx
from app.processors import extract_document
from app.storage.file_storage import FileStorage

router = APIRouter()
logger = logging.getLogger(__name__)


def _generate(file_id: str, template_id: str = "ups-healthcare", slide_count: int = 8, topic_name: str = "", presented_by: str = ""):
    settings = get_settings()
    storage = FileStorage(settings)
    try:
        status = storage.read_status(file_id)
        document = extract_document(Path(status["input_path"]), status["file_name"])
        knowledge = analyze(document)
        try:
            presentation = plan_with_llm(knowledge, document.text, slide_count, settings) if settings.use_llm else plan(knowledge, slide_count)
        except Exception:
            logger.exception("LLM planning failed; using deterministic planner")
            presentation = plan(knowledge, slide_count)
        presentation = review(presentation)
        presentation.presentation.theme.update({"topic_name": topic_name, "presented_by": presented_by})
        output_path = generate_pptx(presentation, storage.output_path(file_id), template_id)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail="Upload not found.") from error
    except Exception as error:
        logger.exception("Presentation generation failed for %s", file_id)
        raise HTTPException(status_code=422, detail=f"Unable to generate presentation: {error}") from error
    status.update({"status": "generated", "template_id": template_id, "slide_count_requested": slide_count, "output_path": str(output_path), "slide_count": len(presentation.presentation.slides), "presentation": presentation.model_dump()})
    storage.write_status(file_id, status)
    return status


@router.post("/generate-presentation/{file_id}")
def generate_presentation(file_id: str, template_id: str = Query(default="ups-healthcare"), slide_count: int = Query(default=8, ge=3, le=20), topic_name: str = Query(default=""), presented_by: str = Query(default="")):
    return _generate(file_id, template_id, slide_count, topic_name, presented_by)


@router.post("/generate-presentation")
def generate_presentation_from_query(file_id: str, template_id: str = Query(default="ups-healthcare"), slide_count: int = Query(default=8, ge=3, le=20), topic_name: str = Query(default=""), presented_by: str = Query(default="")):
    return _generate(file_id, template_id, slide_count, topic_name, presented_by)