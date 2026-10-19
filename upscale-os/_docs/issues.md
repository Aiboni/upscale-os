# GitHub Issues creation backlog
These are DRAFT issues; create them on GitHub after pushing the repo. Do not mark closed before QA verification.

| Title | Label | Goal | Acceptance criteria |
| --- | --- | --- | --- |
| Bootstrap app and passing test | mvp | Start app reliably | API health returns 200; pytest passes |
| Produce responsive design system | mvp | Distinctive visual identity | Desktop/mobile navigation and working modal |
| Build leads CRUD frontend with mock service | mvp | Make contacts manageable | Create, edit, search, filter, delete |
| Define OpenAPI contract | mvp | Formalize REST interface | /docs describes schemas/errors |
| Build memory-store API | mvp | Enable integration without database | Mock API contract test (retrospective optional demo milestone) |
| Implement SQLAlchemy SQLite models | mvp | Persistent data | Restart retains lead/campaign/task changes |
| Connect leads frontend to API | mvp | CRUD through backend | All actions update on reload |
| Build pipeline board | mvp | Advance sales stages | Stage changes saved to DB |
| Build campaigns management | mvp | Track outreach | Create, pause, edit, delete |
| Build tasks manager | mvp | Track follow-ups | Create, check complete, delete |
| Add real KPI analytics | mvp | Surface insights | Stats reflect database edits |
| CSV export and activity feed | mvp | Portable data and audit | Export readable CSV, activity after changes |
| Run user walkthrough and log defects | mvp | Validate app | Run tested flows and file bugs as user-test-bug |
| Add team accounts and authentication | post-mvp | Multi-user access | Password hashing, authorization tests |
| Integrate email provider | post-mvp | Send campaigns | Explicit opt-in, quotas, actual provider state |
| Integrate LinkedIn supported workflow | post-mvp | Social outreach | Compliant API integration and credentials |
| Automatic analytics trend snapshots | post-mvp | Real timeseries | Uses stored daily snapshots, no synthetic chart |
| Docker deploy & uptime checks | post-mvp | Production hosting | Database volume survives container recreation |
