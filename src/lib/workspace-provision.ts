import { createAdminClient } from "@/lib/supabase/admin";
import { createClient } from "@/lib/supabase/server";

function slugify(input: string) {
  const base = input
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return base || "workspace";
}

/**
 * Creates profile + organization + owner membership when a user exists
 * but the signup trigger never ran (common if SQL was applied after signup).
 */
export async function provisionWorkspaceIfMissing(params: {
  userId: string;
  email?: string;
  preferredName?: string | null;
}) {
  const admin = createAdminClient();
  if (!admin) {
    return {
      ok: false as const,
      error:
        "Workspace missing and SUPABASE_SERVICE_ROLE_KEY is not set. Add the service role key to .env.local, or re-run migration 00001 and create a new account.",
    };
  }

  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user || user.id !== params.userId) {
    return { ok: false as const, error: "Not authenticated" };
  }

  const fullName =
    params.preferredName?.trim() ||
    (user.user_metadata?.full_name as string | undefined)?.trim() ||
    params.email?.split("@")[0] ||
    "Agency owner";

  const orgName =
    (user.user_metadata?.organization_name as string | undefined)?.trim() ||
    `${fullName}'s Workspace`;

  const { error: profileError } = await admin.from("profiles").upsert(
    {
      id: params.userId,
      full_name: fullName,
    },
    { onConflict: "id" },
  );

  if (profileError) {
    return { ok: false as const, error: profileError.message };
  }

  const { data: existingMembership } = await admin
    .from("organization_members")
    .select("organization_id")
    .eq("user_id", params.userId)
    .limit(1)
    .maybeSingle();

  if (existingMembership?.organization_id) {
    return { ok: true as const };
  }

  const slug = `${slugify(orgName)}-${params.userId.replace(/-/g, "").slice(0, 8)}`;

  const { data: org, error: orgError } = await admin
    .from("organizations")
    .insert({
      name: orgName,
      slug,
      created_by: params.userId,
    })
    .select("id")
    .single();

  if (orgError || !org) {
    return {
      ok: false as const,
      error:
        orgError?.message ??
        "Could not create organization. Confirm migration 00001 was run.",
    };
  }

  const { error: memberError } = await admin.from("organization_members").insert({
    organization_id: org.id,
    user_id: params.userId,
    role: "owner",
  });

  if (memberError) {
    return { ok: false as const, error: memberError.message };
  }

  return { ok: true as const };
}
