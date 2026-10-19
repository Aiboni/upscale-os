# Upscale OS — B2B Sales Intelligence CRM

A self-hosted, responsive full-stack CRM inspired by the business category of Upscale System LLC (independent student project; not affiliated).

## Features
- Dashboard with live lead/campaign/pipeline metrics
- Lead create, search, filter, edit, delete
- Kanban pipeline with click-to-advance opportunities
- Campaign create, edit, pause/activate, delete, progress metrics
- Task create, mark complete, delete
- Sales analytics, acquisition channel breakdown, CSV export
- Recent activity feed
- SQLite persistence through SQLAlchemy ORM
- OpenAPI 3 docs and interactive API playground at `/docs`

**Limitations:** Campaign messaging is not sent; metrics are local/demo and not connected to email, LinkedIn or Stripe. The dashboard's revenue line is illustrative, while KPI cards use live SQLite data. No authentication; use locally for coursework, not as a publicly exposed multiuser CRM.

## Run locally
Python 3.10+ required.

Windows PowerShell:
```powershell
cd upscale-os
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload
```

macOS/Linux:
```bash
cd upscale-os
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Then open **http://127.0.0.1:8000**. API docs: http://127.0.0.1:8000/docs.

The database is created automatically at `upscale.db`, with initial demo records. New edits persist after server restart. Set `SEED_DEMO=0` for a blank database. Set `DATABASE_URL` to another SQLAlchemy URL for an alternative DB.

## Tests
```bash
pytest -q
```

## Repo setup / GitHub Issues
1. Push this folder to a new GitHub repository.
2. Create labels `mvp`, `post-mvp`, and `user-test-bug`.
3. Create GitHub issues from `_docs/issues.md`; use criteria in `_docs/task-template.md`.
4. Have PM refine issues, engineer implement, QA test and close issues after review.
5. Track real testing bugs as `user-test-bug` and close them after a regression test.

Do not represent seeded demo records, scaffolded issue specs, or local testing as genuine customer activity or pre-closed GitHub issues.


## Public HTTPS URL (Railway)

This project can run on Railway with a persistent SQLite volume. A public URL is issued by Railway after deployment, **not** by running the app on localhost.

1. Create a **private** GitHub repository and upload the project files. Don't upload `.env` or `*.db`.
2. Visit https://railway.com/ and choose **New Project → Deploy from GitHub repo**.
3. Select this repository. Railway uses the project's `Dockerfile` to start the app on the assigned `PORT`.
4. Under the service, add a persistent **Volume**, mounted at `/data`.
5. Set variable `DATABASE_URL=sqlite:////data/upscale.db` and (if you want a blank public demo) `SEED_DEMO=0`.
6. Open **Settings → Networking → Public Networking → Generate Domain**. Railway will display your real `https://...up.railway.app` address.
7. Check the home page and `/docs` on that domain.

**Security:** the app currently has no authentication: anyone with the public URL can access and modify CRM data. Only deploy as a public demo with non-sensitive, fake data. Add login, authorization, and rate limiting before storing any real customer data. Railway pricing and availability may vary.
