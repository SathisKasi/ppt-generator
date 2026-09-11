from typing import Any

from pydantic import BaseModel, Field


class NormalizedDocument(BaseModel):
    file_name: str
    file_type: str
    text: str = ""
    tables: list[Any] = Field(default_factory=list)
    images: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Knowledge(BaseModel):
    subject: str = "Not provided"
    problem: str = "Not provided"
    objectives: list[str] = Field(default_factory=list)
    sections: list[dict[str, object]] = Field(default_factory=list)
    facts: list[str] = Field(default_factory=list)
    numbers: list[str] = Field(default_factory=list)
    dates: list[str] = Field(default_factory=list)
    conclusions: list[str] = Field(default_factory=list)
    source_references: list[str] = Field(default_factory=list)