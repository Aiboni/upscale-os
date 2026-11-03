# Groomed issues (copy into GitHub)

Create each issue in GitHub (**Issues → New issue**), paste the body, add the label. Create the labels `mvp`, `post-mvp`, `user-test-bug` first (**Issues → Labels**).

> **Honesty note:** the backlog was written after the code (retrospective). Issues stay **open** until QA posts a real `## QA: PASS` comment with evidence. Do not close them just because this file exists.

## MVP and post-MVP issues

### 1. Bootstrap app with passing test
**Label:** `mvp`

```markdown
## Goal

The app starts locally and a test proves the API is alive.

## Acceptance criteria

- [ ] `uvicorn app:app` starts without errors and `/` serves the dashboard
- [ ] `GET /api/health` returns 200 with `{"status":"ok"}`
- [ ] `pytest -q` passes on a clean checkout with an empty database
- [ ] GitHub Actions runs the tests on every push

## Out of scope

- Deployment (see Docker/Railway issue)

## Constraints

- Python 3.10+, FastAPI, SQLAlchemy 2
- No extra dependencies
```

### 2. Responsive design system and navigation
**Label:** `mvp`

```markdown
## Goal

The UI has a consistent look and is usable on desktop and phone.

## Acceptance criteria

- [ ] Sidebar navigation on desktop, bottom/mobile navigation at 375px width
- [ ] All six pages (Overview, Leads, Campaigns, Pipeline, Tasks, Analytics) reachable
- [ ] Colours/fonts follow `_docs/design-system.md`
- [ ] Modal opens, closes with the button and with Esc
- [ ] No horizontal page scroll at 375px

## Out of scope

- Language switcher (follow-up issue)

## Constraints

- Stay inside `static/index.html`
```

### 3. Frontend with mock service layer
**Label:** `mvp`

```markdown
## Goal

The whole frontend can run without a backend, so the idea can be judged before the server exists.

## Acceptance criteria

- [ ] Opening `/?mock=1` loads the dashboard using `static/mock-service.js` only
- [ ] Create, edit, delete lead works in mock mode and resets on reload
- [ ] Duplicate email in mock mode shows the same error message as the real API
- [ ] All frontend backend calls go through the single `api()` function
- [ ] Without `?mock=1` the real backend is used

## Out of scope

- Persistence in mock mode

## Constraints

- Mock mirrors `openapi.yml` paths and status codes
```

### 4. Define OpenAPI contract
**Label:** `mvp`

```markdown
## Goal

Frontend and backend agree on every endpoint, request and response.

## Acceptance criteria

- [ ] `openapi.yml` lists all `/api/*` endpoints with methods and schemas
- [ ] `/docs` renders and matches `openapi.yml`
- [ ] Error responses (404, 409, 422) are documented or visible in `/docs`

## Out of scope

- Authentication endpoints (post-mvp)

## Constraints

- Regenerate `openapi.yml` from `/openapi.json` when the API changes
```

### 5. Backend with in-memory store
**Label:** `mvp`

```markdown
## Goal

Frontend and FastAPI work together before a database is involved (retrospective milestone).

## Acceptance criteria

- [ ] Frontend calls the real API for leads, campaigns, tasks, stats
- [ ] No CORS or console errors in the browser
- [ ] Documented in `_docs/process.md` iterations as a historical step

## Out of scope

- Re-implementing an in-memory backend now

## Constraints

- Retrospective: the code went straight to SQLite; do not fabricate history
```

### 6. SQLAlchemy + SQLite persistence
**Label:** `mvp`

```markdown
## Goal

Data survives a server restart.

## Acceptance criteria

- [ ] Models for Lead, Campaign, Task, Activity use the SQLAlchemy ORM
- [ ] `DATABASE_URL` env var selects the database
- [ ] A lead created before restarting `uvicorn` is still there after
- [ ] `SEED_DEMO=0` gives an empty database
- [ ] No SQLite-specific features that block moving to Postgres

## Out of scope

- Postgres + migrations (post-mvp)

## Constraints

- Files: `app.py`
```

### 7. Leads CRUD connected to the API
**Label:** `mvp`

```markdown
## Goal

Contacts can be created, searched, filtered, edited and deleted through the backend.

## Acceptance criteria

- [ ] Create lead with valid name, email, company shows it in the list
- [ ] Duplicate email (any letter case) is rejected with 409 and a visible message
- [ ] Search by name/company/email and filter by stage work
- [ ] Edit changes persist after page refresh
- [ ] Delete asks for confirmation and removes the lead
- [ ] Unknown lead ID returns 404

## Out of scope

- Bulk import

## Constraints

- `app.py`, `tests/`, `static/index.html`
```

### 8. Pipeline board
**Label:** `mvp`

```markdown
## Goal

A deal can be moved through stages and the change is saved.

## Acceptance criteria

- [ ] Board shows columns New, Contacted, Qualified, Proposal, Won with counts
- [ ] Clicking a card moves it to the next stage and persists after refresh
- [ ] A card in Won cannot move further and shows a message
- [ ] Pipeline value on Overview updates after a move

## Out of scope

- Drag and drop

## Constraints

- Uses `PATCH /api/leads/{id}`
```

### 9. Campaign management
**Label:** `mvp`

```markdown
## Goal

Outreach campaigns can be created and tracked.

## Acceptance criteria

- [ ] Create, edit (Manage), pause/activate and delete campaigns
- [ ] Reply rate = replies / contacted, 0% when nothing is contacted
- [ ] Target must be at least 1; replies cannot exceed contacted (422)
- [ ] Progress bar never exceeds 100%

## Out of scope

- Sending real messages (post-mvp)

## Constraints

- Metrics are manual/demo and must stay labelled that way
```

### 10. Task manager
**Label:** `mvp`

```markdown
## Goal

Follow-ups can be created, completed and deleted.

## Acceptance criteria

- [ ] Create task with title, priority and optional due date
- [ ] Empty or whitespace title is rejected
- [ ] Checking a task marks it done and lowers the pending badge
- [ ] Delete removes it; unknown ID returns 404

## Out of scope

- Reminders and notifications

## Constraints

- `tasks` table, `/api/tasks`
```

### 11. Real KPI analytics
**Label:** `mvp`

```markdown
## Goal

Dashboard numbers reflect the database, not hard-coded values.

## Acceptance criteria

- [ ] Total leads, pipeline value, won revenue, active campaigns, reply rate come from `/api/stats`
- [ ] Creating or deleting a lead changes the numbers after refresh
- [ ] Lost leads are excluded from pipeline value
- [ ] Demo/illustrative chart is labelled as illustrative

## Out of scope

- Historical trend snapshots (post-mvp)

## Constraints

- `GET /api/stats`
```

### 12. CSV export and activity feed
**Label:** `mvp`

```markdown
## Goal

Leads can be exported and recent actions are visible.

## Acceptance criteria

- [ ] Export button downloads `upscale-leads.csv` with name, email, company, title, status, source, value
- [ ] Values containing commas or quotes are escaped correctly
- [ ] Creating, updating and deleting a lead adds an entry to Recent activity
- [ ] Feed shows at most 12 newest entries

## Out of scope

- Export of campaigns and tasks

## Constraints

- Export is built client-side from loaded leads
```

### 13. Harden input validation
**Label:** `mvp`

```markdown
## Goal

Invalid data is rejected by the API with 422, not stored.

## Acceptance criteria

- [ ] Invalid email format, blank name/company/title and negative values return 422
- [ ] Unknown stage, source, channel, status or priority returns 422
- [ ] Whitespace around names/emails is trimmed
- [ ] All cases covered by `tests/test_validation.py`

## Out of scope

- Showing field-level 422 messages in the UI (see user-test-bug issue)

## Constraints

- Files: `app.py`, `tests/test_validation.py`
- Pydantic v2 models only
```

### 14. Docker image and Railway deployment
**Label:** `mvp`

```markdown
## Goal

The app runs on a public HTTPS URL with data that survives redeploys.

## Acceptance criteria

- [ ] Docker image builds and starts on the platform `PORT`
- [ ] Railway Volume mounted at `/data`, `DATABASE_URL=sqlite:////data/upscale.db`
- [ ] A test lead is still present after a redeploy
- [ ] Public URL and `/docs` open over HTTPS
- [ ] Repository is public and contains no `.env` or `*.db`

## Out of scope

- Postgres, CI/CD promotion, observability (post-mvp)

## Constraints

- Files: `Dockerfile`, `README.md`
```

### 15. User walkthrough and defect log
**Label:** `mvp`

```markdown
## Goal

A real person clicks through every page and defects are filed.

## Acceptance criteria

- [ ] Every page, form, filter, CSV export tested on desktop and mobile width
- [ ] Browser console checked for errors
- [ ] Each reproducible defect has a `user-test-bug` issue and a regression test
- [ ] Results are recorded in `_docs/testing-report.md` with date and environment

## Out of scope

- Inventing defects to reach a number

## Constraints

- Evidence only from tests actually performed
```

### 16. Team accounts and authentication
**Label:** `post-mvp`

```markdown
## Goal

Multiple users can sign in and only see their workspace.

## Acceptance criteria

- [ ] Password hashing and bearer tokens
- [ ] Authorization tests for every endpoint

## Out of scope

- Billing, invites

## Constraints

- Do not start before MVP is closed
```

### 17. Email provider integration
**Label:** `post-mvp`

```markdown
## Goal

Campaigns can really send email with explicit opt-in.

## Acceptance criteria

- [ ] Provider credentials in env vars, quotas, real delivery status

## Out of scope

- LinkedIn

## Constraints

- Compliance with anti-spam rules
```

### 18. LinkedIn outreach workflow
**Label:** `post-mvp`

```markdown
## Goal

Supported, compliant LinkedIn integration.

## Acceptance criteria

- [ ] Uses official API and credentials; no scraping

## Out of scope

- Email

## Constraints

- Check provider terms first
```

### 19. Daily analytics snapshots
**Label:** `post-mvp`

```markdown
## Goal

Revenue/trend chart uses stored data instead of illustrative values.

## Acceptance criteria

- [ ] Daily snapshot table, chart reads it, no synthetic points

## Out of scope

- Forecasting

## Constraints

- Alembic migration
```

### 20. Postgres, CI/CD and observability
**Label:** `post-mvp`

```markdown
## Goal

Production-grade operations as in the course's deploy/devops articles.

## Acceptance criteria

- [ ] docker-compose with Postgres
- [ ] Dev→prod promotion workflow
- [ ] Metrics/alerting

## Out of scope

- Rewrite of the app

## Constraints

- Only after MVP is verified
```

### 21. EN / RU / KZ language switcher
**Label:** `post-mvp`

```markdown
## Goal

The UI can be shown in English, Russian and Kazakh.

## Acceptance criteria

- [ ] Selector on every page; choice survives refresh
- [ ] Dynamic rows, modals and toasts are translated
- [ ] No missing keys at 375px

## Out of scope

- Translating API error messages

## Constraints

- Re-test all pages (listed as RE-TEST in testing report)
```

## `user-test-bug` drafts

> Source: **code review / API probing of the original `app.py`**, not a browser walkthrough. Confirm each in `/docs` against the *old* version (git history) before filing. The fixes and regression tests are already in this patch; file the issue, link the commit, let QA verify, then close.

### Bug 1. Lead email format is not validated
**Label:** `user-test-bug`

```markdown
## Goal

Invalid input is rejected clearly.

## Description

Creating a lead with `email: "abc"` is accepted.

## Reproduction steps

1. Open `/docs` → `POST /api/leads`
2. Send `{"name":"X","email":"abc","company":"Y"}`

## Expected / actual

Expected: 422. Actual (before fix): 201 and the lead is stored.

## Acceptance criteria

- [ ] Behaviour matches expected
- [ ] Regression test added: `test_lead_rejects_invalid_email`

## Out of scope

- Unrelated validation

## Constraints

- `app.py`, `tests/test_validation.py`
```

### Bug 2. Unknown stage/source/priority values are stored
**Label:** `user-test-bug`

```markdown
## Goal

Invalid input is rejected clearly.

## Description

Any string is accepted for status, source, channel and priority, which breaks the pipeline board and charts.

## Reproduction steps

1. `PATCH /api/leads/{id}` with `{"status":"Hacked"}`

## Expected / actual

Expected: 422. Actual (before fix): 200 and the lead disappears from every pipeline column.

## Acceptance criteria

- [ ] Behaviour matches expected
- [ ] Regression test added: `test_lead_rejects_negative_value_and_unknown_stage`, `test_lead_patch_validation_and_missing_id`

## Out of scope

- Unrelated validation

## Constraints

- `app.py`, `tests/test_validation.py`
```

### Bug 3. Campaign replies can exceed contacted
**Label:** `user-test-bug`

```markdown
## Goal

Invalid input is rejected clearly.

## Description

Replies > contacted gives reply rates above 100%.

## Reproduction steps

1. `PATCH /api/campaigns/{id}` with `{"contacted":5,"replies":9}`

## Expected / actual

Expected: 422 and nothing saved. Actual (before fix): 200, reply rate 180%.

## Acceptance criteria

- [ ] Behaviour matches expected
- [ ] Regression test added: `test_campaign_validation_and_replies_rule`

## Out of scope

- Unrelated validation

## Constraints

- `app.py`, `tests/test_validation.py`
```

### Bug 4. Blank or whitespace-only names are accepted
**Label:** `user-test-bug`

```markdown
## Goal

Invalid input is rejected clearly.

## Description

`name: "   "` and empty PATCH names are stored.

## Reproduction steps

1. `POST /api/leads` with `name` of spaces

## Expected / actual

Expected: 422. Actual (before fix): 201.

## Acceptance criteria

- [ ] Behaviour matches expected
- [ ] Regression test added: `test_lead_rejects_blank_required_text`

## Out of scope

- Unrelated validation

## Constraints

- `app.py`, `tests/test_validation.py`
```

### Bug 5. UI shows 'Request failed' for validation errors
**Label:** `user-test-bug`

```markdown
## Goal

Invalid input is rejected clearly.

## Description

FastAPI returns `detail` as a list for 422; `api()` in `static/index.html` only handles string details.

## Reproduction steps

1. Submit the lead form with an invalid value after validation is enforced

## Expected / actual

Expected: readable message. Actual: generic 'Request failed'.

## Acceptance criteria

- [ ] Behaviour matches expected
- [ ] Regression test added: Manual UI check (not yet fixed)

## Out of scope

- Unrelated validation

## Constraints

- `app.py`, `tests/test_validation.py`
```

### Optional: Revenue period selector does nothing
**Label:** `user-test-bug` — file this **only if you reproduced it yourself** (your earlier report). This zip's `index.html` has no period selector, so it belongs to your newer deployed version. Add your own steps: open Overview → Revenue → click 3/7/12 months → chart does not change; console errors; browser and date.

## QA verdict comment template

```markdown
## QA: PASS|FAIL

- [ ] criterion 1 — PASS|FAIL|NOT VERIFIED
- [ ] criterion 2 — ...

Tests: `py -m pytest -q` → <paste real output>
Environment: local / Railway, date, browser
```
