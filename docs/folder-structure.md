# Folder structure

```
dm-os/
├── docs/
├── public/
├── supabase/
│   └── migrations/
│       └── 00001_init_auth_orgs.sql
├── src/
│   ├── proxy.ts                 # Auth session + route protection (Next.js 16)
│   ├── app/
│   │   ├── actions/auth.ts      # Login / signup / sign-out
│   │   ├── auth/callback/       # Email confirmation callback
│   │   ├── (auth)/login|signup/
│   │   ├── (dashboard)/dashboard/
│   │   ├── setup/               # Supabase setup checklist UI
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── auth/
│   │   ├── ai/                  # Copilot rail
│   │   ├── brand/
│   │   ├── crm/
│   │   ├── foundation/
│   │   ├── layout/              # Sidebar, topbar, dashboard shell
│   │   ├── shared/
│   │   └── ui/
│   ├── lib/
│   │   ├── ai/                  # Copilot prompts + OpenAI helper
│   │   ├── data/
│   │   ├── env.ts               # Includes AI feature flag helpers
│   │   ├── navigation.ts
│   │   ├── workspace.ts
│   │   ├── validations/
│   │   ├── supabase/
│   │   └── utils.ts
│   └── types/database.ts
├── public/
│   ├── dm-logo.png
│   └── favicon.png
├── .env.example
├── CHANGELOG.md
└── README.md
```

## Conventions

| Area | Rule |
|------|------|
| UI primitives | `src/components/ui` only |
| Feature UI | `src/components/<feature>/` |
| Route groups | `(auth)`, `(dashboard)` — no URL segment |
| Shared logic | `src/lib/` |
| SQL | `supabase/migrations/` |
