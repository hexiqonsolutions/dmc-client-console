# API documentation

## Status

Milestone 2 uses **Server Actions** and one **Route Handler** (no public REST API yet).

## Server Actions

### `loginAction(input)`

- **File:** `src/app/actions/auth.ts`
- **Input:** `{ email, password }` (Zod `loginSchema`)
- **Result:** `{ success: true }` or `{ success: false, error }`

### `signupAction(input)`

- **File:** `src/app/actions/auth.ts`
- **Input:** `{ fullName, organizationName, email, password }` (Zod `signupSchema`)
- **Side effect:** Auth user + DB trigger creates profile/org/membership
- **Result:** success, optional “check your email” message, or error

### `signOutAction()`

- Clears Supabase session and redirects to `/login`

## Route Handlers

### `GET /auth/callback`

- Exchanges `?code=` for a session (email confirmation / OAuth-style PKCE)
- Redirects to `/dashboard` (or `?next=`)

## Planned later

REST or Server Actions for clients/projects with Zod validation + org membership checks.
