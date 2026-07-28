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

## Configure Supabase (Milestone 2)

1. Create a project at [supabase.com](https://supabase.com).
2. Open **Project Settings → API** and copy:
   - Project URL → `NEXT_PUBLIC_SUPABASE_URL`
   - `anon` `public` key → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
3. Paste into `.env.local`. Optionally add `SUPABASE_SERVICE_ROLE_KEY` (server-only; not used in Milestone 2 UI).
4. **Authentication → URL Configuration**
   - Site URL: `http://localhost:3000`
   - Redirect URLs: `http://localhost:3000/auth/callback`
5. **Authentication → Providers → Email**  
   For local testing, turn **off** “Confirm email” so signup signs you in immediately.
6. **SQL Editor** → run the full contents of  
   `supabase/migrations/00001_init_auth_orgs.sql`
7. Restart the app:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Verify Milestone 2

1. Home page shows **Milestone 2** and links to Sign in / Get started.  
2. Visit `/setup` — should report keys detected after env is filled.  
3. `/signup` — create account with name, workspace, email, password.  
4. You land on `/dashboard` with workspace name and role `owner`.  
5. Sign out → `/login` works; visiting `/dashboard` while signed out redirects to `/login`.

If organization is missing on the dashboard, the SQL migration did not run — re-run it and create a fresh user.

## Scripts

| Command | Purpose |
|---------|---------|
| `npm run dev` | Development server |
| `npm run build` | Production build |
| `npm run start` | Run production build |
| `npm run lint` | ESLint |

## Troubleshooting

- **Keys missing** → fill `.env.local` and restart.  
- **Port in use** → stop the other process or use the port Next suggests.  
- **Signup works but no org** → re-run SQL migration; existing users won’t get the trigger retroactively (sign up a new user).  
- **Email confirmation loop** → disable confirm email for local, or complete the email link to `/auth/callback`.
