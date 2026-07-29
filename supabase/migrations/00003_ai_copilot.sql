-- DM OS Milestone 5: AI Copilot conversations (org-scoped, RLS)
-- Run after 00001 and 00002 migrations.

create type public.ai_message_role as enum ('user', 'assistant', 'system');

create table if not exists public.ai_conversations (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations (id) on delete cascade,
  user_id uuid not null references auth.users (id) on delete cascade,
  title text not null default 'Copilot chat',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.ai_messages (
  id uuid primary key default gen_random_uuid(),
  conversation_id uuid not null references public.ai_conversations (id) on delete cascade,
  organization_id uuid not null references public.organizations (id) on delete cascade,
  role public.ai_message_role not null,
  content text not null,
  created_at timestamptz not null default now(),
  constraint ai_messages_content_not_blank check (char_length(trim(content)) > 0)
);

create index if not exists ai_conversations_org_user_idx
  on public.ai_conversations (organization_id, user_id, updated_at desc);

create index if not exists ai_messages_conversation_idx
  on public.ai_messages (conversation_id, created_at asc);

drop trigger if exists ai_conversations_set_updated_at on public.ai_conversations;
create trigger ai_conversations_set_updated_at
  before update on public.ai_conversations
  for each row execute function public.set_updated_at();

alter table public.ai_conversations enable row level security;
alter table public.ai_messages enable row level security;

drop policy if exists "ai_conversations_select_own" on public.ai_conversations;
create policy "ai_conversations_select_own"
  on public.ai_conversations for select
  to authenticated
  using (
    user_id = auth.uid()
    and public.is_org_member(organization_id)
  );

drop policy if exists "ai_conversations_insert_own" on public.ai_conversations;
create policy "ai_conversations_insert_own"
  on public.ai_conversations for insert
  to authenticated
  with check (
    user_id = auth.uid()
    and public.is_org_member(organization_id)
  );

drop policy if exists "ai_conversations_update_own" on public.ai_conversations;
create policy "ai_conversations_update_own"
  on public.ai_conversations for update
  to authenticated
  using (
    user_id = auth.uid()
    and public.is_org_member(organization_id)
  )
  with check (
    user_id = auth.uid()
    and public.is_org_member(organization_id)
  );

drop policy if exists "ai_conversations_delete_own" on public.ai_conversations;
create policy "ai_conversations_delete_own"
  on public.ai_conversations for delete
  to authenticated
  using (
    user_id = auth.uid()
    and public.is_org_member(organization_id)
  );

drop policy if exists "ai_messages_select_own_conversation" on public.ai_messages;
create policy "ai_messages_select_own_conversation"
  on public.ai_messages for select
  to authenticated
  using (
    public.is_org_member(organization_id)
    and exists (
      select 1
      from public.ai_conversations c
      where c.id = conversation_id
        and c.user_id = auth.uid()
    )
  );

drop policy if exists "ai_messages_insert_own_conversation" on public.ai_messages;
create policy "ai_messages_insert_own_conversation"
  on public.ai_messages for insert
  to authenticated
  with check (
    public.is_org_member(organization_id)
    and exists (
      select 1
      from public.ai_conversations c
      where c.id = conversation_id
        and c.user_id = auth.uid()
        and c.organization_id = organization_id
    )
  );
