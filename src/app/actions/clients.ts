"use server";

import { revalidatePath } from "next/cache";

import type { ActionResult } from "@/lib/action-result";
import { createClient } from "@/lib/supabase/server";
import { clientSchema, toNullable, type ClientInput } from "@/lib/validations/crm";
import { requireWorkspace } from "@/lib/workspace";

export async function createClientAction(
  input: ClientInput,
): Promise<ActionResult> {
  const parsed = clientSchema.safeParse(input);
  if (!parsed.success) {
    return {
      success: false,
      error: parsed.error.issues[0]?.message ?? "Invalid client data",
    };
  }

  const workspace = await requireWorkspace();
  const supabase = await createClient();

  const { error } = await supabase.from("clients").insert({
    organization_id: workspace.organization.id,
    name: parsed.data.name,
    email: toNullable(parsed.data.email),
    phone: toNullable(parsed.data.phone),
    company: toNullable(parsed.data.company),
    status: parsed.data.status,
    notes: toNullable(parsed.data.notes),
    created_by: workspace.userId,
  });

  if (error) {
    return { success: false, error: error.message };
  }

  revalidatePath("/dashboard");
  revalidatePath("/dashboard/clients");
  revalidatePath("/dashboard/projects");
  return { success: true, message: "Client created" };
}

export async function updateClientAction(
  id: string,
  input: ClientInput,
): Promise<ActionResult> {
  const parsed = clientSchema.safeParse(input);
  if (!parsed.success) {
    return {
      success: false,
      error: parsed.error.issues[0]?.message ?? "Invalid client data",
    };
  }

  const workspace = await requireWorkspace();
  const supabase = await createClient();

  const { error } = await supabase
    .from("clients")
    .update({
      name: parsed.data.name,
      email: toNullable(parsed.data.email),
      phone: toNullable(parsed.data.phone),
      company: toNullable(parsed.data.company),
      status: parsed.data.status,
      notes: toNullable(parsed.data.notes),
    })
    .eq("id", id)
    .eq("organization_id", workspace.organization.id);

  if (error) {
    return { success: false, error: error.message };
  }

  revalidatePath("/dashboard");
  revalidatePath("/dashboard/clients");
  revalidatePath("/dashboard/projects");
  return { success: true, message: "Client updated" };
}

export async function deleteClientAction(id: string): Promise<ActionResult> {
  const workspace = await requireWorkspace();
  const supabase = await createClient();

  const { error } = await supabase
    .from("clients")
    .delete()
    .eq("id", id)
    .eq("organization_id", workspace.organization.id);

  if (error) {
    return { success: false, error: error.message };
  }

  revalidatePath("/dashboard");
  revalidatePath("/dashboard/clients");
  revalidatePath("/dashboard/projects");
  return { success: true, message: "Client deleted" };
}
