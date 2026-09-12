from pptx.dml.color import RGBColor

THEMES = {
    "ups-healthcare": {
        "id": "ups-healthcare",
        "name": "UPS Healthcare Executive",
        "brand_name": "UPS Healthcare",
        "font": "Segoe UI",
        "bg": RGBColor(0xFA, 0xF9, 0xF6),        # Warm off-white
        "primary": RGBColor(0x0D, 0x1F, 0x4D),   # UPS Deep Navy
        "secondary": RGBColor(0x30, 0x15, 0x06), # UPS Classic Brown
        "accent": RGBColor(0xFF, 0xB8, 0x1C),    # UPS Warm Gold
        "card_bg": RGBColor(0xFF, 0xFF, 0xFF),   # Crisp White Card
        "card_border": RGBColor(0xDF, 0xE4, 0xEA),
        "header_bg": RGBColor(0x0D, 0x1F, 0x4D),
        "header_text": RGBColor(0xFF, 0xFF, 0xFF),
        "text_primary": RGBColor(0x0D, 0x1F, 0x4D),
        "text_secondary": RGBColor(0x24, 0x18, 0x0F),
        "text_muted": RGBColor(0x5D, 0x65, 0x74),
        "ink": "24180F",
        "brand": "301506",
        "muted": "5D6574",
        "background": "FAF9F6",
    },
    "clean-corporate": {
        "id": "clean-corporate",
        "name": "Clean Corporate",
        "brand_name": "Clean Corporate",
        "font": "Calibri",
        "bg": RGBColor(0xF0, 0xF4, 0xF8),        # Cool Ice White
        "primary": RGBColor(0x12, 0x30, 0x4A),   # Corporate Deep Navy
        "secondary": RGBColor(0x1E, 0x29, 0x3B), # Slate Navy
        "accent": RGBColor(0x0F, 0x8B, 0x8D),    # Modern Vibrant Teal
        "card_bg": RGBColor(0xFF, 0xFF, 0xFF),   # Pure White Card
        "card_border": RGBColor(0xCB, 0xD5, 0xE1),
        "header_bg": RGBColor(0x12, 0x30, 0x4A),
        "header_text": RGBColor(0xFF, 0xFF, 0xFF),
        "text_primary": RGBColor(0x12, 0x30, 0x4A),
        "text_secondary": RGBColor(0x1E, 0x29, 0x3B),
        "text_muted": RGBColor(0x64, 0x74, 0x8B),
        "ink": "1E293B",
        "brand": "12304A",
        "muted": "64748B",
        "background": "F0F4F8",
    },
    "minimal-light": {
        "id": "minimal-light",
        "name": "Minimal Light",
        "brand_name": "Minimal Light",
        "font": "Arial",
        "bg": RGBColor(0xFF, 0xFF, 0xFF),        # Pure White
        "primary": RGBColor(0x11, 0x18, 0x27),   # Charcoal
        "secondary": RGBColor(0x37, 0x41, 0x51), # Mid Slate
        "accent": RGBColor(0x25, 0x63, 0xEB),    # Electric Royal Blue
        "card_bg": RGBColor(0xF9, 0xFA, 0xFB),   # Soft gray
        "card_border": RGBColor(0xE5, 0xE7, 0xEB),
        "header_bg": RGBColor(0x11, 0x18, 0x27),
        "header_text": RGBColor(0xFF, 0xFF, 0xFF),
        "text_primary": RGBColor(0x11, 0x18, 0x27),
        "text_secondary": RGBColor(0x37, 0x41, 0x51),
        "text_muted": RGBColor(0x6B, 0x72, 0x80),
        "ink": "111827",
        "brand": "111827",
        "muted": "6B7280",
        "background": "FFFFFF",
    },
    "presentation_template": {
        "id": "presentation_template",
        "name": "Presentation Template",
        "brand_name": "Presentation Template",
        "font": "Calibri",
        "bg": RGBColor(0x1A, 0x1A, 0x2E),
        "primary": RGBColor(0x0F, 0x34, 0x60),
        "secondary": RGBColor(0x53, 0x34, 0x83),
        "accent": RGBColor(0xE9, 0x45, 0x60),
        "card_bg": RGBColor(0x16, 0x21, 0x3E),
        "card_border": RGBColor(0x0F, 0x34, 0x60),
        "header_bg": RGBColor(0x0F, 0x34, 0x60),
        "header_text": RGBColor(0xFF, 0xFF, 0xFF),
        "text_primary": RGBColor(0xFF, 0xFF, 0xFF),
        "text_secondary": RGBColor(0xE0, 0xE0, 0xE0),
        "text_muted": RGBColor(0xA0, 0xA0, 0xB0),
        "ink": "E0E0E0",
        "brand": "0F3460",
        "muted": "A0A0B0",
        "background": "1A1A2E",
    },
    "ups_inspired_corporate_ppt_template": {
        "id": "ups_inspired_corporate_ppt_template",
        "name": "UPS Inspired Corporate PPT Template",
        "brand_name": "UPS Healthcare",
        "font": "Segoe UI",
        "bg": RGBColor(0xFA, 0xF9, 0xF6),
        "primary": RGBColor(0x0D, 0x1F, 0x4D),
        "secondary": RGBColor(0x30, 0x15, 0x06),
        "accent": RGBColor(0xFF, 0xB8, 0x1C),
        "card_bg": RGBColor(0xFF, 0xFF, 0xFF),
        "card_border": RGBColor(0xDF, 0xE4, 0xEA),
        "header_bg": RGBColor(0x0D, 0x1F, 0x4D),
        "header_text": RGBColor(0xFF, 0xFF, 0xFF),
        "text_primary": RGBColor(0x0D, 0x1F, 0x4D),
        "text_secondary": RGBColor(0x24, 0x18, 0x0F),
        "text_muted": RGBColor(0x5D, 0x65, 0x74),
        "ink": "24180F",
        "brand": "301506",
        "muted": "5D6574",
        "background": "FAF9F6",
    },
}

THEME = THEMES["ups-healthcare"]


def get_theme(template_id: str) -> dict:
    clean_id = (template_id or "ups-healthcare").lower().strip()
    if clean_id in THEMES:
        return dict(THEMES[clean_id])
    alt_id = clean_id.replace("-", "_")
    if alt_id in THEMES:
        return dict(THEMES[alt_id])
    alt_id2 = clean_id.replace("_", "-")
    if alt_id2 in THEMES:
        return dict(THEMES[alt_id2])
    return dict(THEMES["ups-healthcare"])