from typing import Any

from pydantic import BaseModel, Field


class Visual(BaseModel):
    required: bool = False
    type: str = "none"
    description: str = ""


class Slide(BaseModel):
    slide_number: int
    slide_type: str
    section: str = ""
    title: str = Field(max_length=120)
    purpose: str = ""
    executive_message: str = ""
    layout: str = "content"
    content: list[Any] = Field(default_factory=list)
    visual: Visual = Field(default_factory=Visual)
    data: list[Any] = Field(default_factory=list)
    speaker_notes: str = ""
    source_references: list[str] = Field(default_factory=list)


class Presentation(BaseModel):
    title: str
    subtitle: str = ""
    audience: str = "Not provided"
    purpose: str = ""
    estimated_duration_minutes: int = 20
    theme: dict[str, Any] = Field(default_factory=lambda: {"brand": "UPS Healthcare"})
    slides: list[Slide] = Field(min_length=1)


class PresentationEnvelope(BaseModel):
    presentation: Presentation