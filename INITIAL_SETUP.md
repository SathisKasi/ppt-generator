# Initial Setup

## 1. Prepare Python

Install Python 3.12 or newer and ensure `python` is available in PowerShell:

```powershell
python --version
```

## 2. Start the web application

Run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`, upload `example_input.txt`, and generate a PowerPoint.

## 3. Add business inputs

Start with plain text or JSON while the content model is validated. Keep each source fact traceable. Use labels such as:

```text
Title: Warehouse visibility initiative
Audience: Healthcare operations leadership
Problem: Manual status updates delay exception handling
Objective: Improve visibility of shipment exceptions
```

Do not add assumed metrics, dates, customer names, milestones, or capabilities. Use `Not provided` or `Requires confirmation` when evidence is absent.

## 4. Configure an LLM when needed

The default deterministic path runs without an LLM. For Qwen3 through vLLM or Ollama, set `USE_LLM=true` and configure `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL` in `.env`.

## 5. Configure branding before rendering

Create a future branding configuration containing the approved UPS Healthcare logo, colors, fonts, typography hierarchy, dimensions, layouts, image rules, icon rules, footer, header, and accessibility requirements. The current generator intentionally marks branding as `Configuration required` rather than inventing values.

## 5. Future implementation stages

1. Add adapters for Word, PDF, PowerPoint, Excel, SharePoint, Teams, email, and meeting notes.
2. Normalize all adapters into a common source model with references.
3. Add validation for slide count, title length, bullet length, unsupported claims, and missing sources.
4. Implement a deterministic `python-pptx` renderer that consumes only the JSON contract.
5. Add fixture-based tests and render comparison checks.

## Validation checklist

- The output is valid JSON.
- Every slide has one purpose and one executive message.
- Agenda sections match the generated story.
- Missing facts are explicit.
- Visual requirements describe information-bearing visuals.
- Source references are present on every slide.