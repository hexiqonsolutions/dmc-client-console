# Installation guide

## Prerequisites

- **Node.js** 20+ (LTS recommended)
- **npm** 10+
- Git
- A free [Supabase](https://supabase.com) project (required from Milestone 2)

## Install

```bash
npm install
cp .env.example .env.local
```

## Configure Supabase

1. Create a project at [supabase.com](https://supabase.com).
2. Open **Project Settings → API** and copy:
   - Project URL → `NEXT_PUBLIC_SUPABASE_URL`
   - `anon` `public` key → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
3. Paste into `.env.local`.
4. **Authentication → URL Configuration**
   - Site URL: `http://localhost:3000`
   - Redirect URLs: `http://localhost:3000/auth/callback`
5. **Authentication → Providers → Email**  
   For local testing, turn **off** “Confirm email”.
6. **SQL Editor** → run migrations in order:
   - `supabase/migrations/00001_init_auth_orgs.sql`
   - `supabase/migrations/00002_clients_projects.sql`
   - `supabase/migrations/00003_ai_copilot.sql`
7. Enable Copilot in `.env.local`:

```bash
NEXT_PUBLIC_AI_COPILOT_ENABLED=true
# Optional for live AI:
# OPENAI_API_KEY=sk-...
```

8. Restart the app:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Verify Milestone 5

1. Sign in to the dashboard.
2. Click **Copilot** in the top bar (rail opens).
3. Ask “How do I add a client?” — guided reply appears without OpenAI.
4. With `OPENAI_API_KEY` set, replies switch to live mode.
5. Clear conversation with the trash icon.

If chat fails with a SQL/table error, run `00003_ai_copilot.sql`.

## Scripts

| Command | Purpose |
|---------|---------|
| `npm run dev` | Development server |
| `npm run build` | Production build |
| `npm run start` | Run production build |
| `npm run lint` | ESLint |

## Troubleshooting

- **Keys missing** → fill `.env.local` and restart.
- **Copilot button missing** → set `NEXT_PUBLIC_AI_COPILOT_ENABLED=true` and restart.
- **Clients/projects/AI errors** → run the matching SQL migration.
- **Signup works but no org** → re-run `00001` migration; create a fresh user.
