# Architecture

## What DM OS is

DM OS is a multi-tenant SaaS operating system for a digital agency. It manages clients, projects, delivery workflows, and AI assistance behind a shared design system and secure auth layer.

## Guiding principles

1. **Modular** — features live in clear modules; shared UI/utils are reused, never copied.
2. **Secure by default** — auth, authorization, and validation before data access.
3. **Milestone-driven** — ship thin vertical slices; do not build the entire product at once.
4. **Clean boundaries** — UI → application logic → data access → database.

## High-level layers

```
┌─────────────────────────────────────────┐
│  Presentation (Next.js App Router UI)   │
│  shadcn/ui · RHF · Zod                  │
├─────────────────────────────────────────┤
│  Application (Server Actions / routes)  │
│  validation · auth checks · use-cases   │
├─────────────────────────────────────────┤
│  Edge gate (src/proxy.ts)               │
│  Session refresh · route protection     │
├─────────────────────────────────────────┤
│  Infrastructure                         │
│  Supabase Auth · Postgres · RLS         │
└─────────────────────────────────────────┘
```

## Milestone 2 (current)

- Email/password auth via Supabase
- `src/proxy.ts` refreshes sessions and guards `/dashboard`
- Signup metadata creates **profile + organization + owner membership** (DB trigger)
- Server Actions: login, signup, sign-out
- Auth callback route for email confirmation links

## Auth flow

1. User signs up → Supabase Auth user created  
2. Trigger creates profile + workspace  
3. Session cookie set (or email confirmation first)  
4. Proxy validates with `getUser()` on each matched request  
5. Dashboard layout loads workspace via RLS-filtered queries  

## Multi-tenancy

Organizations own future clients/projects. Users belong to organizations with roles (`owner`, `admin`, `member`). RLS enforces isolation.

## Design system

**Studio Command** tokens live in `src/app/globals.css` and map to shadcn CSS variables.
