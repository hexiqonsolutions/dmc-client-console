# Database schema

## Status

**Milestone 2 implemented.** Apply the SQL migration in Supabase before signing up.

## Migration file

`supabase/migrations/00001_init_auth_orgs.sql`

Run it in: **Supabase Dashboard → SQL → New query → Paste → Run**.

## Tables

### `profiles`

| Column | Type | Notes |
|--------|------|--------|
| id | uuid PK | Matches `auth.users.id` |
| full_name | text | From signup metadata |
| avatar_url | text | Optional |
| created_at / updated_at | timestamptz | Auto |

### `organizations`

| Column | Type | Notes |
|--------|------|--------|
| id | uuid PK | |
| name | text | Workspace display name |
| slug | text unique | URL-safe + user id fragment |
| created_by | uuid | Signup user |
| created_at / updated_at | timestamptz | Auto |

### `organization_members`

| Column | Type | Notes |
|--------|------|--------|
| id | uuid PK | |
| organization_id | uuid FK | → organizations |
| user_id | uuid FK | → auth.users |
| role | org_role | `owner` \| `admin` \| `member` |
| created_at | timestamptz | Auto |
| unique | (organization_id, user_id) | One membership per org |

## Bootstrap on signup

Trigger `on_auth_user_created` runs `handle_new_user()`:

1. Inserts `profiles` row  
2. Creates an organization from `organization_name` metadata  
3. Adds the user as `owner` in `organization_members`

## Relationships

```
auth.users 1──1 profiles
auth.users 1──* organization_members *──1 organizations
```

## Security (RLS)

- Profiles: users can select/update their own row  
- Organizations: members can select; owners/admins can update  
- Members: users can select memberships for orgs they belong to  
- Helper: `is_org_member(org_id)` (security definer)

## Planned next tables

Notifications, audit logs, and billing tables may come later.

## Milestone 5 tables

### `ai_conversations`

| Column | Type | Notes |
|--------|------|--------|
| id | uuid PK | |
| organization_id | uuid FK | Tenant scope |
| user_id | uuid FK | Conversation owner |
| title | text | From first message |
| created_at / updated_at | timestamptz | Auto |

### `ai_messages`

| Column | Type | Notes |
|--------|------|--------|
| id | uuid PK | |
| conversation_id | uuid FK | Cascade delete |
| organization_id | uuid FK | Tenant scope |
| role | ai_message_role | user / assistant / system |
| content | text | Required |
| created_at | timestamptz | Auto |

Migration: `supabase/migrations/00003_ai_copilot.sql`

RLS: users only access their own conversations within orgs they belong to.

## Milestone 4 tables

### `clients`

| Column | Type | Notes |
|--------|------|--------|
| id | uuid PK | |
| organization_id | uuid FK | Tenant scope |
| name | text | Required |
| email / phone / company / notes | text | Optional |
| status | client_status | `active` \| `inactive` \| `prospect` |
| created_by | uuid | Auth user |
| created_at / updated_at | timestamptz | Auto |

### `projects`

| Column | Type | Notes |
|--------|------|--------|
| id | uuid PK | |
| organization_id | uuid FK | Kept in sync with client org via trigger |
| client_id | uuid FK | Cascade delete with client |
| name | text | Required |
| description | text | Optional |
| status | project_status | planned/active/on_hold/completed/cancelled |
| due_date | date | Optional |
| created_by | uuid | Auth user |
| created_at / updated_at | timestamptz | Auto |

Migration: `supabase/migrations/00002_clients_projects.sql`

RLS: members can select/insert/update/delete rows for organizations they belong to.