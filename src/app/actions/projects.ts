"use server";

import { revalidatePath } from "next/cache";

import type { ActionResult } from "@/lib/action-result";
import { createClient } from "@/lib/supabase/server";
import { projectSchema, toNullable, type ProjectInput } from "@/lib/validations/crm";
import { requireWorkspace } from "@/lib/workspace";

export async function createProjectAction(
  input: ProjectInput,
): Promise<ActionResult> {
  const parsed = projectSchema.safeParse(input);
  if (!parsed.success) {
    return {
      success: false,
      error: parsed.error.issues[0]?.message ?? "Invalid project data",
    };
  }

  const workspace = await requireWorkspace();
  const supabase = await createClient();

  const { data: client, error: clientError } = await supabase
    .from("clients")
    .select("id")
    .eq("id", parsed.data.clientId)
    .eq("organization_id", workspace.organization.id)
    .maybeSingle();

  if (clientError || !client) {
    return { success: false, error: "Selected client was not found" };
  }

  const { error } = await supabase.from("projects").insert({
    organization_id: workspace.organization.id,
    client_id: parsed.data.clientId,
    name: parsed.data.name,
    description: toNullable(parsed.data.description),
    status: parsed.data.status,
    due_date: toNullable(parsed.data.dueDate),
    created_by: workspace.userId,
  });

  if (error) {
    return { success: false, error: error.message };
  }

  revalidatePath("/dashboard");
  revalidatePath("/dashboard/projects");
  return { success: true, message: "Project created" };
}

export async function updateProjectAction(
  id: string,
  input: ProjectInput,
): Promise<ActionResult> {
  const parsed = projectSchema.safeParse(input);
  if (!parsed.success) {
    return {
      success: false,
      error: parsed.error.issues[0]?.message ?? "Invalid project data",
    };
  }

  const workspace = await requireWorkspace();
  const supabase = await createClient();

  const { data: client, error: clientError } = await supabase
    .from("clients")
    .select("id")
    .eq("id", parsed.data.clientId)
    .eq("organization_id", workspace.organization.id)
    .maybeSingle();

  if (clientError || !client) {
    return { success: false, error: "Selected client was not found" };
  }

  const { error } = await supabase
    .from("projects")
    .update({
      client_id: parsed.data.clientId,
      name: parsed.data.name,
      description: toNullable(parsed.data.description),
      status: parsed.data.status,
      due_date: toNullable(parsed.data.dueDate),
    })
    .eq("id", id)
    .eq("organization_id", workspace.organization.id);

  if (error) {
    return { success: false, error: error.message };
  }

  revalidatePath("/dashboard");
  revalidatePath("/dashboard/projects");
  return { success: true, message: "Project updated" };
}

export async function deleteProjectAction(id: string): Promise<ActionResult> {
  const workspace = await requireWorkspace();
  const supabase = await createClient();

  const { error } = await supabase
    .from("projects")
    .delete()
    .eq("id", id)
    .eq("organization_id", workspace.organization.id);

  if (error) {
    return { success: false, error: error.message };
  }

  revalidatePath("/dashboard");
  revalidatePath("/dashboard/projects");
  return { success: true, message: "Project deleted" };
}
