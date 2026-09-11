"""Generate an executive presentation specification as JSON.

The output is intentionally renderer-agnostic. A later PowerPoint renderer can
consume this specification without coupling content decisions to slide drawing.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


NOT_PROVIDED = "Not provided"


def _read_source(path: Path) -> tuple[str, list[str]]:
    """Read a text or JSON source and return normalized text plus references."""
    text = path.read_text(encoding="utf-8").strip()
    if path.suffix.lower() == ".json":
        payload = json.loads(text)
        if not isinstance(payload, dict):
            raise ValueError("JSON input must contain an object at the top level.")
        text = str(payload.get("content", "")).strip()
        if not text:
            text = json.dumps(payload, indent=2)
    return text, [str(path)]


def _first_line(text: str) -> str:
    for line in text.splitlines():
        cleaned = line.strip().lstrip("#").strip()
        if cleaned:
            return cleaned[:80]
    return NOT_PROVIDED


def _value(text: str, labels: tuple[str, ...]) -> str:
    for line in text.splitlines():
        label, separator, value = line.partition(":")
        if separator and label.strip().lower() in labels and value.strip():
            return value.strip()
    return NOT_PROVIDED


def _slide(
    number: int,
    slide_type: str,
    section: str,
    title: str,
    purpose: str,
    message: str,
    layout: str,
    content: list[str],
    visual_type: str,
    visual_description: str,
    references: list[str],
) -> dict[str, Any]:
    return {
        "slide_number": number,
        "slide_type": slide_type,
        "section": section,
        "title": title,
        "purpose": purpose,
        "executive_message": message,
        "layout": layout,
        "content": content,
        "visual": {
            "required": visual_type != "none",
            "type": visual_type,
            "description": visual_description,
        },
        "data": [],
        "speaker_notes": "Confirm unsupported details before executive review.",
        "source_references": references,
    }


def build_spec(source_text: str, references: list[str]) -> dict[str, Any]:
    """Build a conservative presentation outline from supplied source text."""
    title = _value(source_text, ("title", "project", "initiative"))
    if title == NOT_PROVIDED:
        title = _first_line(source_text)

    problem = _value(source_text, ("problem", "challenge", "business problem"))
    objective = _value(source_text, ("objective", "goal", "business objective"))
    audience = _value(source_text, ("audience", "stakeholders"))

    slides = [
        _slide(
            1,
            "title",
            "",
            title,
            "Introduce the initiative and establish the decision context.",
            title,
            "title",
            ["Audience: " + audience],
            "none",
            "",
            references,
        ),
        _slide(
            2,
            "executive_summary",
            "Executive overview",
            "Executive Summary",
            "Summarize the problem, proposal, value, and required action.",
            "The initiative requires a confirmed problem, objective, and decision path.",
            "message_with_supporting_points",
            [
                "Problem: " + problem,
                "Why it matters: " + (objective if objective != NOT_PROVIDED else NOT_PROVIDED),
                "Proposed response: Requires confirmation",
                "Expected impact: Requires confirmation",
                "Decision required: Requires confirmation",
            ],
            "kpi_cards",
            "Five compact executive callouts for problem, importance, proposal, impact, and decision.",
            references,
        ),
        _slide(
            3,
            "agenda",
            "Executive overview",
            "Agenda",
            "Orient the audience to the actual story structure.",
            "The discussion moves from context and problem to solution and action.",
            "numbered_sections",
            [
                "01 Context and business problem",
                "02 Objectives and current state",
                "03 Proposed solution and capabilities",
                "04 Value, implementation, and risks",
                "05 Recommendation and next steps",
            ],
            "section_list",
            "Five numbered agenda sections matching the presentation flow.",
            references,
        ),
        _slide(
            4,
            "business_context",
            "Context and problem",
            "Business Context",
            "Establish the business setting using only supplied evidence.",
            "The source material provides context that must be validated before commitment.",
            "two_column",
            ["Context: " + _first_line(source_text), "Evidence: " + NOT_PROVIDED],
            "context_map",
            "A simple context-to-impact map with evidence gaps clearly marked.",
            references,
        ),
        _slide(
            5,
            "business_problem",
            "Context and problem",
            "Business Problem",
            "Make the primary business issue explicit.",
            problem,
            "problem_statement",
            ["Current pain point: " + problem, "Business consequence: " + NOT_PROVIDED],
            "cause_effect",
            "Cause-and-effect chain from the stated problem to business consequence.",
            references,
        ),
        _slide(
            6,
            "objectives",
            "Objectives and current state",
            "Objectives",
            "Translate the stated need into measurable outcomes without inventing targets.",
            objective,
            "objective_cards",
            ["Primary objective: " + objective, "Success measure: " + NOT_PROVIDED],
            "target_cards",
            "Outcome cards with target and measurement fields flagged for confirmation.",
            references,
        ),
        _slide(
            7,
            "current_state",
            "Objectives and current state",
            "Current State",
            "Show what is known about today and expose missing baseline information.",
            "The current-state baseline is not provided and requires confirmation.",
            "before_after",
            ["Known today: " + _first_line(source_text), "Baseline metrics: " + NOT_PROVIDED],
            "before_after",
            "Before-state panel with evidence and explicit baseline gaps.",
            references,
        ),
        _slide(
            8,
            "proposed_solution",
            "Solution and value",
            "Proposed Solution",
            "Describe the proposed response at an executive level.",
            "A proposed solution is not defined in the supplied material.",
            "solution_overview",
            ["Solution concept: Requires confirmation", "Scope: Requires confirmation"],
            "conceptual_architecture",
            "Placeholder architecture showing inputs, solution, and outcomes without invented capabilities.",
            references,
        ),
        _slide(
            9,
            "benefits",
            "Solution and value",
            "Expected Value",
            "Connect the solution to business value and measurable outcomes.",
            "Benefits and quantified impact require source evidence or stakeholder confirmation.",
            "benefit_columns",
            ["Business benefit: " + NOT_PROVIDED, "Expected impact: " + NOT_PROVIDED],
            "benefit_chain",
            "Capability-to-benefit chain with unverified claims clearly marked.",
            references,
        ),
        _slide(
            10,
            "implementation_roadmap",
            "Implementation and action",
            "Implementation Roadmap",
            "Frame the delivery path and identify missing milestones.",
            "A delivery timeline and milestones require confirmation.",
            "roadmap",
            ["Phase 1: Requires confirmation", "Phase 2: Requires confirmation", "Go-live: Requires confirmation"],
            "timeline",
            "Three-phase timeline with owners, dates, and exit criteria to be confirmed.",
            references,
        ),
        _slide(
            11,
            "risks_and_mitigations",
            "Implementation and action",
            "Risks and Considerations",
            "Make delivery risks, dependencies, and assumptions visible before approval.",
            "Risks, dependencies, and assumptions are not provided and need validation.",
            "risk_table",
            ["Risk: " + NOT_PROVIDED, "Mitigation: " + NOT_PROVIDED, "Dependency: " + NOT_PROVIDED],
            "risk_matrix",
            "Risk matrix with likelihood, impact, owner, and mitigation fields.",
            references,
        ),
        _slide(
            12,
            "next_steps",
            "Implementation and action",
            "Recommendation and Next Steps",
            "Close with the action required to progress the initiative.",
            "Confirm the evidence, decision owner, and next action before proceeding.",
            "decision_and_actions",
            ["Recommendation: Requires confirmation", "Decision owner: Requires confirmation", "Next action: Requires confirmation"],
            "decision_path",
            "Decision gate leading to three prioritized next actions.",
            references,
        ),
    ]

    return {
        "presentation": {
            "title": title,
            "subtitle": "Executive presentation specification",
            "audience": audience,
            "purpose": "Transform supplied business information into an executive-ready presentation outline.",
            "estimated_duration_minutes": 20,
            "theme": {
                "brand": "UPS Healthcare",
                "branding_status": "Configuration required",
            },
            "slides": slides,
        }
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a renderer-agnostic presentation specification.")
    parser.add_argument("input", type=Path, help="Text or JSON source file")
    parser.add_argument("-o", "--output", type=Path, default=Path("presentation_spec.json"))
    args = parser.parse_args()

    source_text, references = _read_source(args.input)
    args.output.write_text(json.dumps(build_spec(source_text, references), indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()