# Folder structure

```
dm-os/
├── docs/                      # Project documentation
├── public/                    # Static assets
├── src/
│   ├── app/                   # Next.js App Router
│   │   ├── globals.css        # Design tokens + base styles
│   │   ├── layout.tsx         # Root layout (fonts, metadata)
│   │   └── page.tsx           # Foundation home page
│   ├── components/
│   │   ├── foundation/        # Milestone helpers (token swatches, etc.)
│   │   └── ui/                # shadcn/ui primitives (reusable)
│   ├── hooks/                 # Shared React hooks (future)
│   └── lib/
│       └── utils.ts           # cn() and shared helpers
├── .env.example
├── CHANGELOG.md
├── README.md
├── components.json            # shadcn config
├── package.json
└── tsconfig.json
```

## Conventions

| Area | Rule |
|------|------|
| UI primitives | Only in `src/components/ui` (shadcn) |
| Feature UI | `src/components/<feature>/` |
| Routes | `src/app/(group)/...` as features grow |
| Shared logic | `src/lib/` |
| Docs | `docs/` — keep in sync with milestones |

## Planned (later milestones)

```
src/
  app/
    (auth)/login/...
    (dashboard)/...
  components/
    layout/          # sidebar, topbar
    clients/
    projects/
  lib/
    supabase/        # browser + server clients
    validations/     # Zod schemas
```
