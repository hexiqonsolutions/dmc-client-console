-- DM OS Milestone 4: Clients + Projects (org-scoped, RLS)
-- Run in Supabase SQL Editor after 00001_init_auth_orgs.sql

create type public.client_status as enum ('active', 'inactive', 'prospect');
create type public.project_status as enum (
  'planned',
  'active',
  'on_hold',
  'completed',
  'cancelled'
);

create table if not exists public.clients (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations (id) on delete cascade,
  name text not null,
  email text,
  phone text,
  company text,
  status public.client_status not null default 'active',
  notes text,
  created_by uuid references auth.users (id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint clients_name_not_blank check (char_length(trim(name)) > 0)
);

create table if not exists public.projects (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations (id) on delete cascade,
  client_id uuid not null references public.clients (id) on delete cascade,
  name text not null,
  description text,
  status public.project_status not null default 'planned',
  due_date date,
  created_by uuid references auth.users (id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint projects_name_not_blank check (char_length(trim(name)) > 0)
);

create index if not exists clients_organization_id_idx
  on public.clients (organization_id);

create index if not exists clients_name_idx
  on public.clients (organization_id, lower(name));

create index if not exists projects_organization_id_idx
  on public.projects (organization_id);

create index if not exists projects_client_id_idx
  on public.projects (client_id);

create index if not exists projects_status_idx
  on public.projects (organization_id, status);

drop trigger if exists clients_set_updated_at on public.clients;
create trigger clients_set_updated_at
  before update on public.clients
  for each row execute function public.set_updated_at();

drop trigger if exists projects_set_updated_at on public.projects;
create trigger projects_set_updated_at
  before update on public.projects
  for each row execute function public.set_updated_at();

-- Keep project.organization_id aligned with its client.
create or replace function public.enforce_project_org_matches_client()
returns trigger
language plpgsql
as $$
declare
  client_org uuid;
begin
  select organization_id into client_org
  from public.clients
  where id = new.client_id;

  if client_org is null then
    raise exception 'Client not found';
  end if;

  if new.organization_id is distinct from client_org then
    new.organization_id := client_org;
  end if;

  return new;
end;
$$;

drop trigger if exists projects_enforce_org on public.projects;
create trigger projects_enforce_org
  before insert or update on public.projects
  for each row execute function public.enforce_project_org_matches_client();

alter table public.clients enable row level security;
alter table public.projects enable row level security;

drop policy if exists "clients_select_member" on public.clients;
create policy "clients_select_member"
  on public.clients for select
  to authenticated
  using (public.is_org_member(organization_id));

drop policy if exists "clients_insert_member" on public.clients;
create policy "clients_insert_member"
  on public.clients for insert
  to authenticated
  with check (public.is_org_member(organization_id));

drop policy if exists "clients_update_member" on public.clients;
create policy "clients_update_member"
  on public.clients for update
  to authenticated
  using (public.is_org_member(organization_id))
  with check (public.is_org_member(organization_id));

drop policy if exists "clients_delete_member" on public.clients;
create policy "clients_delete_member"
  on public.clients for delete
  to authenticated
  using (public.is_org_member(organization_id));

drop policy if exists "projects_select_member" on public.projects;
create policy "projects_select_member"
  on public.projects for select
  to authenticated
  using (public.is_org_member(organization_id));

drop policy if exists "projects_insert_member" on public.projects;
create policy "projects_insert_member"
  on public.projects for insert
  to authenticated
  with check (public.is_org_member(organization_id));

drop policy if exists "projects_update_member" on public.projects;
create policy "projects_update_member"
  on public.projects for update
  to authenticated
  using (public.is_org_member(organization_id))
  with check (public.is_org_member(organization_id));

drop policy if exists "projects_delete_member" on public.projects;
create policy "projects_delete_member"
  on public.projects for delete
  to authenticated
  using (public.is_org_member(organization_id));
