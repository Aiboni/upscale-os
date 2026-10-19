# Upscale OS agent instructions
Read `_docs/plan.md`, `_docs/process.md`, and `_docs/design-system.md` before changes. GitHub Issues (once created) are the single backlog. Tackle one issue at a time; have PM groom criteria, engineer implement, QA run regression tests and verify manually. Never claim tests or issue closure without performing them.
Commands: `pip install -r requirements.txt`; `pytest -q`; `uvicorn app:app --reload`.
Maintain SQLite via SQLAlchemy ORM, keep FastAPI `/docs` up to date, do not represent synthetic analytics as real. Run tests for changes and add regression tests for bugs.
