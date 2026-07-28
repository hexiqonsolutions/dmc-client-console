# API documentation

## Status

Milestone 4 uses **Server Actions** (no public REST API yet).

## Auth actions

### `loginAction` / `signupAction` / `signOutAction`

- **File:** `src/app/actions/auth.ts`
- Zod-validated email/password flows

## CRM actions

### Clients — `src/app/actions/clients.ts`

| Action | Input | Notes |
|--------|-------|--------|
| `createClientAction` | `ClientInput` | Inserts into caller's organization |
| `updateClientAction` | `id`, `ClientInput` | Org-scoped update |
| `deleteClientAction` | `id` | Cascades related projects in DB |

### Projects — `src/app/actions/projects.ts`

| Action | Input | Notes |
|--------|-------|--------|
| `createProjectAction` | `ProjectInput` | Verifies client belongs to org |
| `updateProjectAction` | `id`, `ProjectInput` | Org-scoped update |
| `deleteProjectAction` | `id` | Org-scoped delete |

Schemas: `src/lib/validations/crm.ts`

All mutations call `requireWorkspace()`, rely on Supabase RLS, and `revalidatePath` dashboard routes.

## Route Handlers

### `GET /auth/callback`

- Exchanges `?code=` for a session
- Redirects to `/dashboard` (or `?next=`)
