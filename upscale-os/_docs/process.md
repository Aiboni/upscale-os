# Development process
- Use GitHub issues as canonical tasks after importing the backlog in `_docs/issues.md`.
- Labels: `mvp`, `post-mvp`, `user-test-bug`.
- PM writes checkable acceptance criteria and failure paths before coding.
- Engineer implements smallest independent change and adds tests.
- QA runs automated tests and actual browser walkthrough; file failures as `user-test-bug`.
- Only close a GitHub issue after verifying its acceptance criteria; do not retroactively invent completed GitHub activity.
- Commit after meaningful changes, keep `_docs` in version control.
