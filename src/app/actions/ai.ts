"use server";

import type { ActionResult } from "@/lib/action-result";
import {
  buildCopilotSystemPrompt,
  buildGuidedCopilotReply,
  generateOpenAiReply,
} from "@/lib/ai/copilot";
import { getOpenAiApiKey, isAiCopilotEnabled } from "@/lib/env";
import { createClient } from "@/lib/supabase/server";
import { copilotAskSchema, type CopilotAskInput } from "@/lib/validations/ai";
import { requireWorkspace } from "@/lib/workspace";
import type { AiMessage } from "@/types/database";

export type CopilotAskResult =
  | {
      success: true;
      conversationId: string;
      reply: string;
      mode: "openai" | "guided";
      messages: Pick<AiMessage, "id" | "role" | "content" | "created_at">[];
    }
  | { success: false; error: string };

async function getWorkspaceSnapshot(organizationId: string, orgName: string) {
  const supabase = await createClient();

  const [{ count: clientCount }, { count: projectCount }, { count: activeProjectCount }] =
    await Promise.all([
      supabase
        .from("clients")
        .select("*", { count: "exact", head: true })
        .eq("organization_id", organizationId),
      supabase
        .from("projects")
        .select("*", { count: "exact", head: true })
        .eq("organization_id", organizationId),
      supabase
        .from("projects")
        .select("*", { count: "exact", head: true })
        .eq("organization_id", organizationId)
        .eq("status", "active"),
    ]);

  return {
    organizationName: orgName,
    clientCount: clientCount ?? 0,
    projectCount: projectCount ?? 0,
    activeProjectCount: activeProjectCount ?? 0,
  };
}

export async function askCopilotAction(
  input: CopilotAskInput,
): Promise<CopilotAskResult> {
  if (!isAiCopilotEnabled()) {
    return {
      success: false,
      error: "AI Copilot is disabled. Set NEXT_PUBLIC_AI_COPILOT_ENABLED=true.",
    };
  }

  const parsed = copilotAskSchema.safeParse(input);
  if (!parsed.success) {
    return {
      success: false,
      error: parsed.error.issues[0]?.message ?? "Invalid message",
    };
  }

  const workspace = await requireWorkspace();
  const supabase = await createClient();
  const orgId = workspace.organization.id;

  let conversationId = parsed.data.conversationId ?? null;

  if (conversationId) {
    const { data: existing } = await supabase
      .from("ai_conversations")
      .select("id")
      .eq("id", conversationId)
      .eq("organization_id", orgId)
      .eq("user_id", workspace.userId)
      .maybeSingle();

    if (!existing) {
      conversationId = null;
    }
  }

  if (!conversationId) {
    const title =
      parsed.data.message.length > 48
        ? `${parsed.data.message.slice(0, 45)}...`
        : parsed.data.message;

    const { data: created, error: createError } = await supabase
      .from("ai_conversations")
      .insert({
        organization_id: orgId,
        user_id: workspace.userId,
        title,
      })
      .select("id")
      .single();

    if (createError || !created) {
      return {
        success: false,
        error:
          createError?.message ??
          "Could not start a conversation. Run migration 00003_ai_copilot.sql.",
      };
    }

    conversationId = created.id;
  }

  const { error: userMessageError } = await supabase.from("ai_messages").insert({
    conversation_id: conversationId,
    organization_id: orgId,
    role: "user",
    content: parsed.data.message,
  });

  if (userMessageError) {
    return { success: false, error: userMessageError.message };
  }

  const snapshot = await getWorkspaceSnapshot(orgId, workspace.organization.name);
  const apiKey = getOpenAiApiKey();
  let reply: string;
  let mode: "openai" | "guided" = "guided";

  try {
    if (apiKey) {
      const { data: history } = await supabase
        .from("ai_messages")
        .select("role, content")
        .eq("conversation_id", conversationId)
        .order("created_at", { ascending: true })
        .limit(20);

      const messages = [
        {
          role: "system" as const,
          content: buildCopilotSystemPrompt(snapshot),
        },
        ...(history ?? [])
          .filter((item) => item.role === "user" || item.role === "assistant")
          .map((item) => ({
            role: item.role as "user" | "assistant",
            content: item.content,
          })),
      ];

      reply = await generateOpenAiReply({ apiKey, messages });
      mode = "openai";
    } else {
      reply = buildGuidedCopilotReply(parsed.data.message, snapshot);
    }
  } catch (error) {
    return {
      success: false,
      error:
        error instanceof Error
          ? error.message
          : "Copilot could not generate a reply",
    };
  }

  const { error: assistantError } = await supabase.from("ai_messages").insert({
    conversation_id: conversationId,
    organization_id: orgId,
    role: "assistant",
    content: reply,
  });

  if (assistantError) {
    return { success: false, error: assistantError.message };
  }

  await supabase
    .from("ai_conversations")
    .update({ updated_at: new Date().toISOString() })
    .eq("id", conversationId);

  const { data: messages } = await supabase
    .from("ai_messages")
    .select("id, role, content, created_at")
    .eq("conversation_id", conversationId)
    .order("created_at", { ascending: true });

  return {
    success: true,
    conversationId,
    reply,
    mode,
    messages: messages ?? [],
  };
}

export async function clearCopilotConversationAction(
  conversationId: string,
): Promise<ActionResult> {
  if (!isAiCopilotEnabled()) {
    return { success: false, error: "AI Copilot is disabled" };
  }

  const workspace = await requireWorkspace();
  const supabase = await createClient();

  const { error } = await supabase
    .from("ai_conversations")
    .delete()
    .eq("id", conversationId)
    .eq("organization_id", workspace.organization.id)
    .eq("user_id", workspace.userId);

  if (error) {
    return { success: false, error: error.message };
  }

  return { success: true, message: "Conversation cleared" };
}
