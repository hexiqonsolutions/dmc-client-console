# Changelog

All notable changes to DM OS are documented here.

## [0.5.0] — 2026-07-29

### Added

- Milestone 5 AI Copilot rail (feature-flagged)
- Guided mode without OpenAI + live mode with `OPENAI_API_KEY`
- SQL migration `00003_ai_copilot.sql` for conversations/messages with RLS
- Dashboard Copilot toggle, empty/loading chat states, clear conversation

## [0.4.0] — 2026-07-28

### Added

- Milestone 4 CRM: clients and projects CRUD with Zod validation
- SQL migration `00002_clients_projects.sql` with org-scoped RLS
- Searchable tables, create/edit dialogs, delete confirmation, toasts
- Dashboard CRM snapshot counts

## [0.3.0] — 2026-07-28

### Added

- Milestone 3 app shell: active nav, sticky topbar, mobile sheet navigation
- Brand logo + favicon wiring (`BrandLogo`, `src/app/icon.png`)
- Shared `PageHeader`, `EmptyState`, `PageLoading`, `ErrorState` patterns
- Placeholder Clients, Projects, and Settings routes with empty states

### Fixed

- Pinned `lucide-react@0.525.0` for Next.js Turbopack compatibility

## [0.2.0] — 2026-07-28

### Added

- Milestone 2 auth: Supabase email/password login and signup
- Organization bootstrap via SQL trigger (profile + workspace + owner)
- Protected `/dashboard` via `src/proxy.ts` session refresh
- Auth callback route, setup checklist page, dashboard workspace summary
- React Hook Form + Zod validation on auth forms
- SQL migration `supabase/migrations/00001_init_auth_orgs.sql`

## [0.1.0] — 2026-07-28

### Added

- Milestone 1 foundation: Next.js App Router, TypeScript, Tailwind CSS v4, ESLint
- shadcn/ui with button, card, badge, and separator
- Studio Command design tokens (teal + ink + mist)
- Space Grotesk + Manrope typography
- Foundation home page with token and component smoke tests
- Documentation set under `docs/`
- `.env.example` for upcoming Supabase and app config
