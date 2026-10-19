# Product specification — Upscale OS

## Origin
Inspired by TrustMRR's listing for Upscale System LLC, a B2B CRM and lead-generation business. This is an original teaching project, not a copy or affiliated product.

## Problem
Small B2B teams juggle lead information in spreadsheets, outreach plans in documents, and follow-ups in their heads. They lack a centralized view of their pipeline and next actions.

## User
Founder-led sales and small business-development teams, first releasing as a local single-workspace demo.

## MVP user journeys
1. See live totals and recent activity in the dashboard.
2. Create/search/filter/edit/delete leads, each with company, title, source, stage, value.
3. Advance deals through New → Contacted → Qualified → Proposal → Won in the board.
4. Create and manage outreach campaigns with channel, target, contacted, replies and status.
5. Create and complete tasks and review metrics.
6. Export lead list as CSV; all persisted in SQLite.

## Explicit exclusions
No actual outbound message delivery; no third-party integrations, real AI, authentication, billing, team invites, or real-time collaborative sync. Visual trend chart is illustrative and labeled as such.

## Quality requirements
Responsive desktop/mobile layout, input validation and HTTP errors, SQLAlchemy ORM, OpenAPI, automated API tests, reproducible setup.

## Iteration history
Iteration 1: design-ready frontend and demo workflows.
Iteration 2: FastAPI endpoints and typed request contracts.
Iteration 3: SQLAlchemy SQLite persistence and action audit feed.
Iteration 4: end-to-end API smoke tests, documentation, deployment prep.
