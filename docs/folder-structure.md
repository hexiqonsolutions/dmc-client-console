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
│   │   ├── brand/               # BrandLogo (dm-logo + favicon)
│   │   ├── foundation/
│   │   ├── layout/              # Sidebar, topbar, mobile nav
│   │   ├── shared/              # PageHeader, EmptyState, loading/error
│   │   └── ui/                  # shadcn primitives
│   ├── lib/
│   │   ├── env.ts
│   │   ├── navigation.ts
│   │   ├── workspace.ts
│   │   ├── validations/auth.ts
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
