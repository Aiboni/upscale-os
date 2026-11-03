---
name: qa-verify
description: Verify a GitHub issue against its acceptance criteria and post a PASS/FAIL verdict
---

# QA verify

1. Read the issue and its acceptance criteria (`gh issue view <n>`).
2. Run `pytest -q`; copy the exact command and result.
3. Start the app (`uvicorn app:app`) and exercise each criterion: success path, empty/invalid input, duplicates, nonexistent IDs, refresh.
4. Write the verdict comment using the format in `_docs/team/qa-engineer.md`. Do not edit code.
5. If a new defect is found, open an issue labelled `user-test-bug` (Goal, Description, repro steps, expected/actual).
6. Only a PASS allows the orchestrator to close the issue.
