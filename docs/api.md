# API documentation

## Status

**No product APIs yet.** Milestone 1 is UI/foundation only.

## Planned approach

| Style | When to use |
|-------|-------------|
| Server Actions | Form mutations tied to UI (preferred for many CRUD flows) |
| Route Handlers (`src/app/api/...`) | Webhooks, external integrations, streaming |
| Supabase client | Direct authenticated reads where RLS is sufficient |

## Conventions (when APIs appear)

1. Validate input with **Zod** before any database call.
2. Check **auth session** and **org membership**.
3. Return typed, predictable error shapes.
4. Never expose `SUPABASE_SERVICE_ROLE_KEY` to the browser.

This file will list endpoints and payloads as they are built.
