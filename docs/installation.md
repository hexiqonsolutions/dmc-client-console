# Installation guide

## Prerequisites

- **Node.js** 20+ (LTS recommended)
- **npm** 10+
- Git

Check versions:

```bash
node -v
npm -v
```

## Install

From the project root:

```bash
npm install
cp .env.example .env.local
```

Milestone 1 does not require Supabase keys. Leave those blank until Milestone 2.

## Run locally

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

You should see the DM OS foundation page with:

- Brand header
- Foundation checklist
- Design token swatches
- Button / badge smoke test

## Other scripts

| Command | Purpose |
|---------|---------|
| `npm run dev` | Development server |
| `npm run build` | Production build |
| `npm run start` | Run production build |
| `npm run lint` | ESLint |

## Troubleshooting

- **Port in use** — Next.js will offer another port, or stop the other process on 3000.
- **Font/CSS look wrong** — hard refresh; confirm `src/app/globals.css` is imported in `layout.tsx`.
- **Install fails** — delete `node_modules` and `package-lock.json`, then `npm install` again.
