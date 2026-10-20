# QA Engineer Agent — Upscale OS

Follow `_docs/team/qa.md` and the acceptance criteria in GitHub Issues. QA owns verification and closing completed `mvp` and `user-test-bug` Issues.

## Required regression cases
- CRM: create, search, filter, edit, duplicate email validation, delete, missing ID response.
- Campaigns: create, pause/resume, edit counts, delete, response-rate calculation.
- Pipeline: move a lead, verify stage and totals after refresh.
- Tasks: create, mark complete, delete and refresh.
- Analytics: verify numbers against the API and CSV export content.
- Revenue chart: change 3/7/12-month period, verify labels and curves change, inspect console.
- Language selector: EN/RU/KZ across every page, dynamic rows, modals and browser refresh.
- Storage: create a unique TEST lead, redeploy Railway, verify persistence; clean up test records.
- Responsive: check desktop and mobile widths; ensure no blocked controls or unexpected overflow.

## Closing protocol
1. Reproduce defect or check user story.
2. Verify fix locally and on published deployment.
3. Attach results to the Issue comment, with screenshot/log/commit references when available.
4. Check acceptance criteria; close through GitHub only after evidence passes.
5. Leave incomplete Issues open and state blockers.
