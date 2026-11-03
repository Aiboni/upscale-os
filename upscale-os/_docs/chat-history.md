# Upscale OS — brainstorming record

**Important:** this is a reconstructed *summary*, not a verbatim export. If the instructor needs the literal conversation,
export the original chat (ChatGPT/Claude → share or export) and attach it next to this file. Nothing below is invented dialogue.
See also `brainstorm-history.md` (shorter summary) and `plan.md` (the resulting specification).

## Origin
- Assignment: choose a non-trivial idea different from Part I; follow the course articles (spec-driven development, mock→backend→database iterations, GitHub Issues with `mvp` / `post-mvp` / `user-test-bug`, SQLite via an ORM, tests, public repository).
- User chose **Upscale System LLC** from TrustMRR (B2B CRM / lead generation) as inspiration and asked for a beautiful, creative, genuinely working site.
- Assistant proposed **Upscale OS**, an original B2B sales CRM (not a copy of the company site): leads, campaigns, pipeline, tasks, analytics.

## Decisions
| Decision | Reason |
|---|---|
| B2B sales CRM | Non-trivial, several interacting workflows |
| FastAPI + SQLAlchemy + SQLite | Persistence, ORM, OpenAPI for free |
| Demo metrics labelled as demo | No real Stripe/email/LinkedIn integrations |
| English UI first, EN/RU/KZ later | Core product first |
| Railway + Volume | Simple public HTTPS URL with persistent SQLite |

## Later changes
Public link instead of localhost, personal branding, Railway deployment, EN/RU/KZ switcher, Revenue selector bug report and fix attempt, persistence check after redeploy.
