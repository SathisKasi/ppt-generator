import json
from copy import deepcopy

from app.config import Settings
from app.llm.client import LLMClient
from app.llm.prompts import PLANNING_PROMPT
from app.models.document_model import Knowledge
from app.models.presentation_model import PresentationEnvelope


def _fit_slides(slides: list[dict], slide_count: int) -> list[dict]:
    slide_count = max(3, min(slide_count, 20))
    if slide_count == 3:
        return [slides[0], slides[1], slides[-1]]
    if len(slides) < slide_count:
        result = list(slides)
        while len(result) < slide_count:
            source = deepcopy(result[-1])
            source["title"] = f"{source['title']} (continued)"
            source["purpose"] = "Additional supporting detail from the source."
            source["executive_message"] = "Additional supporting detail from the source."
            result.append(source)
        return result
    middle_count = slide_count - 2
    indexes = [round(index * (len(slides) - 1) / (middle_count + 1)) for index in range(1, middle_count + 1)]
    if len(slides) == slide_count:
        return slides
    return [slides[0], *(slides[index] for index in indexes), slides[-1]]


def plan(knowledge: Knowledge, slide_count: int | None = None) -> PresentationEnvelope:
    if slide_count is None:
        slide_count = 15 if len(knowledge.sections) >= 3 else 8
    source = knowledge.source_references
    title = knowledge.subject
    problem = knowledge.problem
    objective = knowledge.objectives[0] if knowledge.objectives else "Not provided"
    def slide(number: int, kind: str, title_text: str, message: str, content: list[str], visual: str) -> dict:
        return {
            "slide_number": number, "slide_type": kind, "section": "",
            "title": title_text, "purpose": message, "executive_message": message,
            "layout": "content", "content": content,
            "visual": {"required": visual != "none", "type": visual, "description": visual},
            "data": [], "speaker_notes": "Validate source evidence before presenting.",
            "source_references": source,
        }
    if len(knowledge.sections) >= 3:
        slides = [slide(1, "title", title, "Introduce the source subject.", [], "none")]
        available = max(1, slide_count - 1)
        groups = [knowledge.sections[index::available] for index in range(available)]
        groups = [group for group in groups if group]
        for number, group in enumerate(groups, start=2):
            section_lines = [str(value) for section in group for value in section.get("lines", [])]
            section_title = " / ".join(str(section["title"]) for section in group)[:120]
            content = section_lines[:5] or ["Not provided"]
            message = next((value for value in section_lines if len(value) > 40), section_title)
            slides.append(slide(number, "content", section_title, message, content, "summary"))
    else:
        slides = [
            slide(1, "title", title, "Introduce the source subject.", [], "none"),
            slide(2, "executive_summary", "Executive Summary", "The source identifies a business issue and an objective requiring validation.", [f"Problem: {problem}", f"Objective: {objective}", "Expected impact: Requires confirmation"], "summary"),
            slide(3, "business_problem", "Business Problem", problem, [problem], "cause_effect"),
            slide(4, "objectives", "Objectives", objective, knowledge.objectives[:5] or ["Not provided"], "target_cards"),
            slide(5, "current_state", "Current State", "The current state is represented by the supplied evidence.", knowledge.facts[:5] or ["Not provided"], "before_after"),
            slide(6, "benefits", "Expected Value", "Quantified benefits require confirmation from the source or stakeholders.", ["Business benefit: Requires confirmation", "Metrics: " + (", ".join(knowledge.numbers) or "Not provided")], "benefit_chain"),
            slide(7, "risks", "Risks and Considerations", "Assumptions and delivery risks require confirmation.", ["Risks: Not provided", "Dependencies: Not provided"], "risk_matrix"),
            slide(8, "next_steps", "Recommendation and Next Steps", "Confirm the evidence and decision required to proceed.", ["Recommendation: Requires confirmation", "Next action: Requires confirmation"], "decision_path"),
        ]
    payload = {"presentation": {"title": title, "subtitle": "AI-generated presentation", "audience": "Not provided", "purpose": "Create an executive presentation from supplied business evidence.", "estimated_duration_minutes": 15, "theme": {"brand": "UPS Healthcare", "branding_status": "Configuration required"}, "slides": _fit_slides(slides, slide_count)}}
    for number, slide_model in enumerate(payload["presentation"]["slides"], start=1):
        slide_model["slide_number"] = number
    return PresentationEnvelope.model_validate(payload)


def plan_with_llm(knowledge: Knowledge, document_text: str, slide_count: int, settings: Settings) -> PresentationEnvelope:
    prompt = PLANNING_PROMPT.format(
        slide_count=slide_count,
        knowledge=json.dumps(knowledge.model_dump(), ensure_ascii=True),
        document=document_text,
    )
    payload = LLMClient(settings).generate_json(prompt)
    presentation = PresentationEnvelope.model_validate(payload)
    presentation.presentation.slides = presentation.presentation.slides[:slide_count]
    while len(presentation.presentation.slides) < slide_count:
        fallback = plan(knowledge, slide_count)
        presentation.presentation.slides.append(fallback.presentation.slides[len(presentation.presentation.slides)])
    for number, slide_model in enumerate(presentation.presentation.slides, start=1):
        slide_model.slide_number = number
    return presentation