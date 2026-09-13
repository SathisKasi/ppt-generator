from app.config import Settings
from app.presentation.template_catalog import get_template, list_templates


def test_static_templates_are_available():
    templates = list_templates(Settings())
    assert {template["id"] for template in templates} >= {
        "ups-healthcare",
        "clean-corporate",
        "minimal-light",
        "test-dev-template",
    }
    assert get_template(Settings(), "clean-corporate")["name"] == "Clean Corporate"
    test_template = get_template(Settings(), "test-dev-template")
    assert test_template["name"] == "Test_dev template"
    assert test_template["accent"] == "DC2626"
    assert test_template["brand"] == "1D4ED8"


def test_powerpoint_template_is_discoverable():
    template = get_template(Settings(), "presentation_template")
    assert template["path"] is not None
    assert template["path"].suffix == ".pptx"