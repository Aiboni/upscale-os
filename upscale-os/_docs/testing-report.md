# Upscale OS — QA Evidence & Test Report

**Status: IN PROGRESS — do not treat unverified items as passes.**

## Evidence already reported in project discussion
| Test | Evidence | Status |
|---|---|---|
| Automated backend pytest | User terminal screenshot showed `2 passed, 3 warnings in 0.80s` | PASS (at time of screenshot) |
| GitHub code push | User terminal screenshots showed successful `git push origin main` | PASS |
| Railway deployment | User screenshot showed deployment ACTIVE / Online and HTTPS site open | PASS (at time of screenshot) |
| SQLite persistence | User confirmed test lead remained after Railway Redeploy | PASS (reported manual test) |
| Revenue period selector | User reported click did nothing; fix subsequently committed, but end-to-end behavior not conclusively verified | RE-TEST REQUIRED |
| EN / RU / KZ switcher | Installation and push confirmed in terminal; full navigation/form checks not established | RE-TEST REQUIRED |
| All other web UI interactions | No comprehensive documented walkthrough yet | NOT VERIFIED |

## Manual test checklist — fill in *after* executing
- [ ] Dashboard: page loads without browser console errors; metrics match `/api/stats`.
- [ ] Leads: create, edit, search, filter, delete and duplicate email behavior.
- [ ] Campaigns: create, manage, pause, reactivate, delete, verify numbers.
- [ ] Sales pipeline: move a test lead to next stage and confirm persistence.
- [ ] Tasks: create, finish, delete and verify refresh.
- [ ] Analytics: charts / metrics and CSV download verified.
- [ ] Revenue period selector: select 3/7/12 months and confirm changed graph and labels.
- [ ] EN/RU/KZ: translations remain through navigation and refresh; dynamic content and dialogs checked.
- [ ] Responsive: desktop and mobile viewport layouts tested.
- [ ] Railway storage: test lead persists after redeploy, with Volume `/data` and configured `DATABASE_URL`.
- [ ] Regression: rerun `py -m pytest -v`, capture fresh output and attach relevant logs.

## Defect reporting workflow
For every reproducible bug, create a GitHub Issue labeled `user-test-bug` containing Goal, Description, reproduction steps, expected/actual results, acceptance criteria and proposed regression tests. Request PM grooming and QA retesting. Do not invent bugs to fulfill a count.

## Issue closure rule
Only close an `mvp` or `user-test-bug` issue after QA can cite passing evidence for every acceptance criterion. Leave `post-mvp` open unless explicitly delivered and tested.
