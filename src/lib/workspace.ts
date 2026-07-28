import { createClient } from "@/lib/supabase/server";
import type { Organization, Profile } from "@/types/database";

export type WorkspaceContext = {
  userId: string;
  email: string | undefined;
  profile: Profile | null;
  organization: Organization | null;
  role: string | null;
};

export async function getWorkspaceContext(): Promise<WorkspaceContext | null> {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return null;
  }

  const { data: profile } = await supabase
    .from("profiles")
    .select("*")
    .eq("id", user.id)
    .maybeSingle();

  const { data: membership } = await supabase
    .from("organization_members")
    .select("role, organization_id")
    .eq("user_id", user.id)
    .order("created_at", { ascending: true })
    .limit(1)
    .maybeSingle();

  let organization: Organization | null = null;

  if (membership?.organization_id) {
    const { data: org } = await supabase
      .from("organizations")
      .select("*")
      .eq("id", membership.organization_id)
      .maybeSingle();
    organization = org;
  }

  return {
    userId: user.id,
    email: user.email,
    profile: profile ?? null,
    organization,
    role: membership?.role ?? null,
  };
}
