# Architecture

## What DM OS is

DM OS is a multi-tenant SaaS operating system for a digital agency. It will manage clients, projects, delivery workflows, and AI assistance behind a shared design system and secure auth layer.

## Guiding principles

1. **Modular** — features live in clear modules; shared UI/utils are reused, never copied.
2. **Secure by default** — auth, authorization, and validation before data access.
3. **Milestone-driven** — ship thin vertical slices; do not build the entire product at once.
4. **Clean boundaries** — UI → application logic → data access → database.

## High-level layers (target)

```
┌─────────────────────────────────────────┐
│  Presentation (Next.js App Router UI)   │
│  shadcn/ui · RHF · Zod · TanStack Query │
├─────────────────────────────────────────┤
│  Application (server actions / API)     │
│  validation · auth checks · use-cases   │
├─────────────────────────────────────────┤
│  Infrastructure                         │
│  Supabase Auth · Postgres · Storage     │
└─────────────────────────────────────────┘
```

## Milestone 1 (current)

Only the **presentation foundation** exists:

- App shell fonts and global CSS tokens
- Base shadcn components
- Docs and env template

No database or auth yet (Milestone 2).

## Multi-tenancy (planned)

Organizations (agency workspaces) own clients and projects. Users belong to organizations with roles. Row Level Security (RLS) in Supabase will enforce isolation.

## Design system

**Studio Command** tokens live in `src/app/globals.css` and map to shadcn CSS variables so every component inherits brand colors automatically.
