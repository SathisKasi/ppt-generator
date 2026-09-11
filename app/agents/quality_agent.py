from app.models.presentation_model import PresentationEnvelope


def review(presentation: PresentationEnvelope) -> PresentationEnvelope:
    slides = presentation.presentation.slides
    for number, slide in enumerate(slides, start=1):
        slide.slide_number = number
        if len(slide.content) > 5:
            slide.content = slide.content[:5]
    return presentation