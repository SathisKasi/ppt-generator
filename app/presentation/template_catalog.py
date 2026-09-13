import json
from pathlib import Path

from app.config import Settings


TEMPLATE_DIRECTORY = Path(__file__).resolve().parents[2] / "templates"


DEFAULT_TEMPLATES = [
    {
        "id": "ups-healthcare",
        "name": "UPS Healthcare Executive",
        "description": "Warm executive layout with UPS Healthcare colors.",
        "file": "ups_healthcare.json",
    },
    {
        "id": "clean-corporate",
        "name": "Clean Corporate",
        "description": "Neutral navy and teal layout for general business content.",
        "file": "clean_corporate.json",
    },
    {
        "id": "minimal-light",
        "name": "Minimal Light",
        "description": "High-contrast white layout for concise presentations.",
        "file": "minimal_light.json",
    },
    {
        "id": "test-dev-template",
        "name": "Test_dev template",
        "description": "Sample red and blue presentation theme for testing.",
        "file": "test_dev_template.json",
    },
    
]


def list_templates(settings: Settings) -> list[dict]:
    directory = TEMPLATE_DIRECTORY
    templates = []
    for item in DEFAULT_TEMPLATES:
        metadata = dict(item)
        config_path = directory / item["file"]
        if config_path.is_file():
            metadata.update(json.loads(config_path.read_text(encoding="utf-8")))
        templates.append(metadata)
    for path in directory.glob("*.pptx"):
        template_id = path.stem.lower().replace(" ", "-")
        if not any(item["id"] == template_id for item in templates):
            templates.append({"id": template_id, "name": path.stem.replace("_", " ").title(), "description": "Uploaded PowerPoint template.", "file": path.name})
    return templates


def get_template(settings: Settings, template_id: str) -> dict:
    template = next((item for item in list_templates(settings) if item["id"] == template_id), None)
    if template is None:
        raise ValueError(f"Unknown presentation template: {template_id}")
    path = TEMPLATE_DIRECTORY / template["file"]
    template["path"] = path if path.suffix.lower() == ".pptx" and path.is_file() else None
    return template