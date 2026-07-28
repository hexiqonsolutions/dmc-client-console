# Deployment guide

## Recommended host

**Vercel** pairs naturally with Next.js App Router.

## Before first deploy

1. Push the repo to GitHub.
2. Create a Vercel project linked to the repo.
3. Add environment variables from `.env.example` (Supabase keys from Milestone 2 onward).
4. Set `NEXT_PUBLIC_APP_URL` to your production domain.

## Deploy steps (Vercel)

1. Import repository in Vercel.
2. Framework preset: **Next.js** (auto-detected).
3. Build command: `npm run build`
4. Output: Next.js default
5. Deploy

## Checklist

- [ ] Production env vars set (no secrets in git)
- [ ] `npm run build` succeeds locally
- [ ] Auth redirect URLs configured in Supabase (Milestone 2+)
- [ ] Custom domain + HTTPS

## Alternative hosts

Any Node host that supports Next.js 16 (Railway, Render, self-hosted Node) can work. Prefer a platform with first-class Next.js support for App Router and Server Actions.

Milestone 1 can be deployed as a static-capable marketing/foundation page; full SaaS deploy becomes meaningful once auth and database exist.
