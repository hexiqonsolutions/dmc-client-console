# DM OS (DM Creatives Operating System)

AI-powered operating system for DM Creatives Studio — modular, secure, and built for production SaaS use.

## Current status

**Milestone 1 — Foundation** is complete.

- Next.js App Router + TypeScript
- Tailwind CSS v4 + shadcn/ui
- Studio Command design system
- Project documentation baseline

## Quick start

```bash
npm install
cp .env.example .env.local
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Documentation

| Doc | Purpose |
|-----|---------|
| [Installation](docs/installation.md) | Install and run locally |
| [Architecture](docs/architecture.md) | System design |
| [Folder structure](docs/folder-structure.md) | Code layout |
| [Environment variables](docs/environment-variables.md) | Config reference |
| [Database schema](docs/database-schema.md) | Data model (planned) |
| [API](docs/api.md) | API surface (planned) |
| [Deployment](docs/deployment.md) | Ship to production |
| [Future improvements](docs/future-improvements.md) | Roadmap |
| [Changelog](CHANGELOG.md) | Release history |

## Stack

- Next.js (App Router) · TypeScript · Tailwind CSS · shadcn/ui
- Supabase (from Milestone 2)
- React Hook Form · Zod · TanStack Query (as features need them)

## Design system

**Studio Command** — deep teal primary (`#0F766E`), ink sidebar (`#0B1220`), cool mist canvas (`#F5F7FA`), Space Grotesk + Manrope.
