# Upscale OS — QA evidence & test report

**Status: IN PROGRESS.** Items are PASS only where evidence is listed. Update this file after every real run.

## Evidence reported by the project owner (not re-executed by the assistant)
| Test | Evidence | Status |
|---|---|---|
| Backend pytest | Terminal screenshot earlier: `2 passed, 3 warnings` | PASS at that time; **re-run needed** (suite changed) |
| Push to GitHub | `git push origin main` succeeded | PASS |
| Railway deployment | Screenshot: ACTIVE / HTTPS site opens | PASS at that time |
| SQLite persistence | Owner reports a test lead survived Railway redeploy | PASS (manual, reported) |
| Revenue period selector | Owner reported click did nothing; fix committed | **RE-TEST REQUIRED** |
| EN/RU/KZ switcher | Installed and pushed; full navigation not checked | **RE-TEST REQUIRED** |
| All other UI interactions | No documented walkthrough yet | NOT VERIFIED |

## Checks performed while preparing this patch (honest log)
| Check | Result |
|---|---|
| `static/mock-service.js` smoke test with Node (create lead lower-cases email, duplicate → 409, missing ID → 404, stats, delete) | PASS (`mock ok`) |
| `app.py` and `tests/test_validation.py` parse as valid Python | PASS |
| `pytest` on the new validation tests | **NOT RUN** — dependencies could not be installed in the preparation environment. Run `py -m pytest -q` locally and paste the real output below. |
| Findings from reading the original `app.py` | Invalid emails, arbitrary stage names, replies > contacted, blank names were accepted. Drafted as `user-test-bug` in `_docs/issues-groomed.md`; fixed with regression tests. Not browser-tested. |

## Latest local pytest run (fill in)
```
Date:
Command: py -m pytest -q
Result:
```

## Manual checklist — tick only after doing it
- [ ] Dashboard loads without console errors; metrics match `/api/stats`
- [ ] Leads: create, edit, search, filter, delete, duplicate email, invalid email message
- [ ] Campaigns: create, manage, pause/activate, delete, reply rate
- [ ] Pipeline: move a lead, refresh, still moved
- [ ] Tasks: create, complete, delete
- [ ] Analytics + CSV export opens in Excel with correct columns
- [ ] Mock mode `/?mock=1` works without database
- [ ] Revenue period selector 3/7/12 months changes the chart
- [ ] EN/RU/KZ on every page, modals and refresh
- [ ] Mobile width 375px: no overflow, no blocked controls
- [ ] Railway: test lead persists after redeploy (Volume `/data`)

## Defect workflow
Reproducible bug → GitHub Issue `user-test-bug` (Goal, Description, steps, expected/actual) → PM grooms → Engineer fixes + regression test → QA posts PASS/FAIL → close only after PASS.

## Local pytest run (2026-11-03, Windows, Python 3.14)
Command: py -m pytest -q
Result: 18 passed, 3 warnings in 1.66s (warnings: FastAPI on_event deprecation)

