# UPSCALE OS — Final QA Report

**Project:** UPSCALE OS — B2B Sales Intelligence Platform  
**Author / tester:** Aibek Mekhlisov  
**Report date:** 20 October 2026  
**Environment:** Public Railway deployment — https://upscale-os-production.up.railway.app  
**Repository:** https://github.com/Aiboni/upscale-os  
**Scope:** Reported manual acceptance testing and previously recorded automated backend testing

## 1. Executive summary

**Result: PASS for the eight scenarios reported by the tester.** The tester confirmed that EN/RU/KZ language switching, the revenue chart period selector, lead management, campaign management, sales pipeline updates, task management, analytics display, and SQLite persistence after Railway redeployment work as expected.

**New defects in this test round:** None reported. A previously discovered bug with the revenue period selector was fixed and the tester now reports that selecting a period changes the graph.

This report distinguishes **user-confirmed manual results** from direct automated or independently observed test evidence. It does not certify untested edge cases, security, accessibility, mobile layouts, or production load.

## 2. Manual test results

| ID | Area | Test performed / acceptance condition | Result | Evidence type |
|---|---|---|---|---|
| M-01 | Internationalization | EN, RU, and KZ can be selected and translated UI appears | PASS | User-confirmed manual test |
| M-02 | Dashboard chart | Changing the “Last 7 months” selector changes the chart period | PASS | User-confirmed manual retest |
| M-03 | Leads | Create, edit, and delete leads | PASS | User-confirmed manual test |
| M-04 | Campaigns | Create and edit campaigns | PASS | User-confirmed manual test |
| M-05 | Sales pipeline | Move deals between stages | PASS | User-confirmed manual test |
| M-06 | Tasks | Create tasks and mark them complete | PASS | User-confirmed manual test |
| M-07 | Analytics | Statistics appear and display correctly | PASS | User-confirmed manual test |
| M-08 | Database persistence | Data remains after Railway redeployment | PASS | User-confirmed manual test |

**Manual test summary:** 8 passed / 0 failed / 0 newly reported defects **within the scenarios above**.

## 3. Automated tests

The earlier VS Code pytest run displayed `2 passed, 3 warnings in 0.80s` after a Windows SQLite temporary-directory cleanup issue was corrected. The two recorded tests cover an API CRUD roundtrip and frontend/OpenAPI availability. This is **historical evidence**, not a fresh automated run conducted while producing this document.

To collect a new traceable result from the repository root containing `app.py`, execute:

```powershell
py -m pytest -v --tb=short | Tee-Object -FilePath _docs/pytest-final-output.txt
```

Record the latest results below after running:

- Fresh run date/time: **Pending**
- Fresh run result: **Pending**
- Test log committed to GitHub: **Pending**

## 4. Previously discovered defect

**GitHub Issue #12:** [Fix revenue period selector not responding](https://github.com/Aiboni/upscale-os/issues/12)

- **Original observed behavior:** Clicking the “Last 7 months” control did not update the chart.
- **Cause identified during code inspection:** The original UI control had no working event handler.
- **Fix:** Period selector and `updateRevenueChart` JavaScript logic were added.
- **Retest:** Tester now reports that selecting a different period updates the graph (**PASS, user-confirmed**).
- **Regression recommendation:** Add an automated browser test asserting both axis labels and chart paths change after a selection.

## 5. Areas not yet certified

The following should **not** be represented as fully tested without additional evidence:

- Responsive behavior across actual phone/tablet widths.
- Accessibility and keyboard navigation.
- Browser JavaScript console free of errors in all flows.
- Leads search/filter and duplicate-email error UI.
- Campaign deletion, pause/resume, and response-rate calculation edge cases.
- Task deletion, negative inputs, and invalid state handling.
- CSV export validity and non-ASCII text.
- Complete translation of all modals, validation errors, and dynamic messages.
- Authentication, authorization, and protection of sensitive CRM data (currently outside the MVP / not implemented).
- Performance, backup/restore and multi-user behavior.

## 6. GitHub Issues and workflow

The development issues and the user-test-bug have been tracked in the repository. **Closing an issue is administrative evidence, not a substitute for acceptance testing.** QA should provide test output or notes mapped to each issue's acceptance criteria. Future features labeled `post-mvp` should not be described as delivered unless implemented and tested.

If any new error is discovered:

1. Open an issue labeled `user-test-bug` with **Goal**, **Description**, reproducible steps, expected/actual outcome and acceptance criteria.
2. Ask the PM agent to groom the report, and QA to add regression test cases.
3. Implement the fix; rerun relevant tests; attach evidence.
4. Close the issue only after successful retesting.

## 7. Final QA assessment

**The eight manually tested workflows pass based on the tester's report, and no additional bugs were reported in this round.** The application has an accessible public deployment and evidence of basic automated backend tests. The MVP is ready for an instructor demonstration of the verified flows, **subject to** collecting a fresh test log and not claiming untested scenarios are certified. This document should be updated if further defects or test results emerge.

---

**QA sign-off:** Aibek Mekhlisov — manual scenario results reported on 20 October 2026.  
**Independent full-system certification:** Not performed.
