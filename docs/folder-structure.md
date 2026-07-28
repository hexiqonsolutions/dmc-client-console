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
│   │   ├── auth/                # Forms + auth shell
│   │   ├── foundation/
│   │   ├── layout/              # Dashboard sidebar
│   │   └── ui/                  # shadcn primitives
│   ├── lib/
│   │   ├── env.ts
│   │   ├── workspace.ts
│   │   ├── validations/auth.ts
│   │   ├── supabase/            # browser, server, middleware clients
│   │   └── utils.ts
│   └── types/database.ts
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
