ANALYSIS_PROMPT = """Extract only supported facts from this document. Return JSON with subject, problem, objectives, facts, numbers, dates, conclusions. Document:\n{document}"""
PLANNING_PROMPT = """Create exactly {slide_count} consolidated presentation slides from the supplied document and extracted knowledge. Use only supported facts. Return a PresentationEnvelope-compatible JSON object with a presentation.slides array containing exactly {slide_count} slides. Each slide needs slide_number, slide_type, title, executive_message, content, visual, and source_references. Choose visual values such as summary, comparison, timeline, process, architecture, metrics, or takeaway when appropriate. Return only valid JSON.

Knowledge:
{knowledge}

Document:
{document}"""