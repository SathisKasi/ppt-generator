from app.agents.presentation_planner import plan
from app.models.document_model import Knowledge
from app.models.presentation_model import PresentationEnvelope


def generate(knowledge: Knowledge) -> PresentationEnvelope:
    return plan(knowledge)