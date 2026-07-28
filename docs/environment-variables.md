# Environment variables

## Setup

1. Copy `.env.example` to `.env.local`
2. Fill values as milestones require them
3. Never commit `.env.local` or real secrets

```bash
cp .env.example .env.local
```

## Reference

| Variable | Required | Milestone | Description |
|----------|----------|-----------|-------------|
| `NEXT_PUBLIC_APP_NAME` | Optional | 1 | Display name (default DM OS) |
| `NEXT_PUBLIC_APP_URL` | Optional | 1 | Public app URL |
| `NEXT_PUBLIC_SUPABASE_URL` | Yes (from M2) | 2 | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Yes (from M2) | 2 | Public anon key (RLS-protected) |
| `SUPABASE_SERVICE_ROLE_KEY` | Server only | 2+ | Admin key — never expose to client |
| `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` | Optional | 5+ | AI providers |

## Naming rules

- `NEXT_PUBLIC_*` — safe to expose in the browser
- All other keys — server-only (Route Handlers, Server Actions, server components)
