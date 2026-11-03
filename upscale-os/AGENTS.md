# Upscale OS — agent instructions

B2B sales CRM: FastAPI + SQLAlchemy + SQLite backend, single-page HTML frontend in `static/`.

## Commands
- `pip install -r requirements.txt` — install dependencies (Windows: `py -m pip install -r requirements.txt`)
- `pytest -q` — whole suite (Windows: `py -m pytest -q`)
- `pytest tests/test_validation.py` — one file
- `uvicorn app:app --reload` — run locally at http://127.0.0.1:8000 (API docs at `/docs`)
- Open `http://127.0.0.1:8000/?mock=1` — frontend against the in-memory mock service (no database)

## Rules
- GitHub Issues are the only backlog. Work on one issue at a time.
- Read the acceptance criteria before starting and before closing.
- Keep SQLite access through the SQLAlchemy ORM. Do not add dependencies without asking.
- Keep FastAPI `/docs` and `openapi.yml` in sync with the code.
- Synthetic/demo metrics must never be presented as real customer data.
- Every bug fix gets a regression test. Never claim tests passed or an issue is closed without running/verifying.
- Commit regularly, one meaningful change per commit, reference the issue (`#12`).

## Documents
- `_docs/process.md` — roles, lifecycle, orchestrator rules
- `_docs/plan.md` — product specification
- `_docs/task-template.md` — template for every groomed issue
- `_docs/design-system.md` — read for anything touching the UI
- `_docs/testing-report.md` — QA evidence log; update after real test runs
- `_docs/team/pm.md`, `_docs/team/software-engineer.md`, `_docs/team/qa-engineer.md` — role definitions
- `.agents/skills/` — reusable procedures (skills)
