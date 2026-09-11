# AI Presentation Generator

FastAPI POC that turns PDF, DOCX, PPTX, XLSX, CSV, TXT, Markdown, and image uploads into validated presentation JSON and a deterministic `.pptx` file. The model decides what to present; Python controls how it is rendered.

## Requirements

- Python 3.12 or newer
- Dependencies listed in `requirements.txt`

## Run

From this directory, create an environment and start the web application:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`, upload a supported file, choose a presentation template and slide count, select **Generate presentation**, and download the resulting PowerPoint.

API endpoints are `GET /health`, `GET /api/templates`, `POST /api/upload`, `POST /api/generate-presentation?file_id={id}&template_id={template_id}&slide_count={count}`, and `GET /api/download/{file_id}`.

The deterministic agent path runs without a model server. For consolidation and slide planning with an open-source model such as Qwen3 through vLLM or Ollama, set `USE_LLM=true`, `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL` in `.env`; `app/llm/client.py` uses an OpenAI-compatible endpoint. If the model is unavailable, generation falls back to the deterministic planner.

## Presentation templates

The dropdown is populated by `GET /api/templates`. Built-in static templates are stored in `templates/` as JSON theme definitions: UPS Healthcare Executive, Clean Corporate, and Minimal Light. The selected template controls the generated deck's colors, fonts, footer accent, and metadata.

To use a real PowerPoint base template, place a `.pptx` file in `templates/`. Its filename becomes the template ID and it appears automatically in the dropdown. During generation, the renderer opens that file and adds the generated slides to the selected deck.

## Project files

- `app/processors`: file extraction adapters
- `app/agents`: analysis, planning, content, and quality stages
- `app/presentation`: deterministic `python-pptx` renderer
- `app/static`: upload and generation web UI
- `tests`: extraction, API, and end-to-end pipeline tests

## Current scope

Run tests with `pytest`. Build with `docker build -t ai-presentation-generator .` and run with `docker run --env-file .env -p 8000:8000 ai-presentation-generator`, or use `docker compose up --build`. Supply approved UPS Healthcare colors, fonts, logo, layouts, and accessibility rules before production use; the current theme marks branding as requiring confirmation.