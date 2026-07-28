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
7. Restart the app:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Verify Milestone 4

1. Sign in → `/dashboard/clients`
2. Add a client → success toast → row appears
3. Edit and delete with confirmation
4. `/dashboard/projects` → create a project linked to that client
5. Search filters both tables
6. If tables are missing, the error state tells you to run `00002_clients_projects.sql`

## Scripts

| Command | Purpose |
|---------|---------|
| `npm run dev` | Development server |
| `npm run build` | Production build |
| `npm run start` | Run production build |
| `npm run lint` | ESLint |

## Troubleshooting

- **Keys missing** → fill `.env.local` and restart.
- **Clients/projects error** → run Milestone 4 SQL migration.
- **Signup works but no org** → re-run `00001` migration; create a fresh user.
- **Email confirmation loop** → disable confirm email for local, or use `/auth/callback`.
