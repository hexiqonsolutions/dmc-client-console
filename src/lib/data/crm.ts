import { createClient } from "@/lib/supabase/server";
import type { Client, ProjectWithClient } from "@/types/database";

export async function listClients(organizationId: string): Promise<Client[]> {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("clients")
    .select("*")
    .eq("organization_id", organizationId)
    .order("name", { ascending: true });

  if (error) {
    throw new Error(error.message);
  }

  return data ?? [];
}

export async function listProjects(
  organizationId: string,
): Promise<ProjectWithClient[]> {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("projects")
    .select("*, clients(id, name, company)")
    .eq("organization_id", organizationId)
    .order("updated_at", { ascending: false });

  if (error) {
    throw new Error(error.message);
  }

  return (data as ProjectWithClient[] | null) ?? [];
}
