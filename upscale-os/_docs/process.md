# Development process

- Tasks are GitHub Issues, one at a time. Labels: `mvp`, `post-mvp`, `user-test-bug`.
- Read the acceptance criteria before starting and before closing.
- Commit regularly.

## Roles
- **PM** — grooms a task before anyone implements it; follows `_docs/team/pm.md`
- **Engineer** — implements one groomed task; follows `_docs/team/software-engineer.md`
- **QA** — checks the result against the acceptance criteria and posts PASS or FAIL; follows `_docs/team/qa-engineer.md`

## Orchestrator
The main session is the orchestrator. It launches PM, Engineer and QA as subagents (fresh context each)
and does not groom, implement or test itself.

### Lifecycle
1. Pick the next open issue from the backlog.
2. PM grooms it (template: `_docs/task-template.md`).
3. Engineer implements it and comments what was done. The issue stays open.
4. QA verifies it and posts a `## QA: PASS` or `## QA: FAIL` comment.
5. On FAIL, back to step 3 with the QA comment as input.
6. On PASS, the orchestrator closes the issue.
7. Repeat until the backlog is empty.

### Rules
- Do not skip step 2.
- The engineer never closes an issue.
- QA never fixes code; it only reports PASS/FAIL with evidence.
- Only close an issue after a QA PASS comment exists.
- Real defects found by testing become issues labelled `user-test-bug`, each with a regression test.

## Iterations (mock → backend → database)
1. Frontend runs against `static/mock-service.js` (`?mock=1`), no server needed.
2. `openapi.yml` records the frontend/backend contract; FastAPI `/docs` is the live version.
3. FastAPI backend replaces the mock; frontend uses the single `api()` function in `static/index.html`.
4. SQLAlchemy + SQLite persistence replaces the in-memory data; `DATABASE_URL` selects the database.
5. Docker image + Railway volume for public deployment.

## Honesty note
This project was started before the issue backlog existed. The backlog in `_docs/issues-groomed.md`
was written afterwards (retrospectively), and issues are only closed after QA re-verifies each one.
