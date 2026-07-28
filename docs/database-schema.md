# Database schema

## Status

**Not implemented yet.** Database work starts in **Milestone 2** with Supabase Postgres.

## Planned core entities

| Table | Purpose |
|-------|---------|
| `organizations` | Tenant / agency workspace |
| `profiles` | User profile linked to auth.users |
| `organization_members` | User ↔ org membership + role |
| `clients` | Agency clients |
| `projects` | Projects belonging to clients |

## Planned relationships

```
organizations 1──* organization_members *──1 profiles
organizations 1──* clients 1──* projects
```

## Security

All tenant tables will use **Row Level Security (RLS)** so users only see data for organizations they belong to.

Schema SQL and typed models will be added when Milestone 2 begins.
