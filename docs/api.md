# API documentation

## Status

DM OS uses **Server Actions** (no public REST API yet).

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

## AI Copilot actions

### `askCopilotAction` — `src/app/actions/ai.ts`

- Requires `NEXT_PUBLIC_AI_COPILOT_ENABLED=true`
- Input: `{ conversationId?, message }` (Zod `copilotAskSchema`)
- Creates/uses an org-scoped conversation, stores user + assistant messages
- Mode:
  - `openai` when `OPENAI_API_KEY` is set
  - `guided` otherwise (local workspace-aware replies)
- Returns conversation id, reply, mode, and message history

### `clearCopilotConversationAction(conversationId)`

- Deletes the caller's conversation (messages cascade)

## Route Handlers

### `GET /auth/callback`

- Exchanges `?code=` for a session
- Redirects to `/dashboard` (or `?next=`)
