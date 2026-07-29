export type CopilotWorkspaceSnapshot = {
  organizationName: string;
  clientCount: number;
  projectCount: number;
  activeProjectCount: number;
};

export function buildCopilotSystemPrompt(snapshot: CopilotWorkspaceSnapshot) {
  return [
    "You are DM OS Copilot, an assistant for a digital agency operating system.",
    "Help with clients, projects, delivery workflow, and using DM OS.",
    "Be concise, practical, and professional. Do not invent private client data.",
    `Workspace: ${snapshot.organizationName}.`,
    `Clients: ${snapshot.clientCount}. Projects: ${snapshot.projectCount} (${snapshot.activeProjectCount} active).`,
    "If asked to change data, explain which screen to use (Clients or Projects) instead of claiming you changed records.",
  ].join(" ");
}

export function buildGuidedCopilotReply(
  message: string,
  snapshot: CopilotWorkspaceSnapshot,
): string {
  const lower = message.toLowerCase();

  if (lower.includes("client")) {
    return [
      `You currently have ${snapshot.clientCount} client${snapshot.clientCount === 1 ? "" : "s"} in ${snapshot.organizationName}.`,
      "Open Dashboard → Clients to add, edit, search, or delete clients.",
      "Each client is private to your organization via Row Level Security.",
      "",
      "Tip: create a client before creating projects — every project must belong to a client.",
    ].join("\n");
  }

  if (lower.includes("project")) {
    return [
      `You currently have ${snapshot.projectCount} project${snapshot.projectCount === 1 ? "" : "s"} (${snapshot.activeProjectCount} active).`,
      "Open Dashboard → Projects to manage status and due dates.",
      "Statuses: planned, active, on hold, completed, cancelled.",
      "",
      "Need OpenAI-powered answers? Add OPENAI_API_KEY to `.env.local` and restart.",
    ].join("\n");
  }

  if (lower.includes("help") || lower.includes("what can")) {
    return [
      "I can help you navigate DM OS:",
      "• Clients — CRM records for your agency",
      "• Projects — delivery work tied to clients",
      "• Settings — workspace overview",
      "",
      `Workspace snapshot: ${snapshot.clientCount} clients, ${snapshot.projectCount} projects.`,
      "Ask about clients, projects, or next steps for your agency workflow.",
    ].join("\n");
  }

  return [
    "I'm running in guided mode (no OpenAI key configured).",
    `Workspace: ${snapshot.organizationName} · ${snapshot.clientCount} clients · ${snapshot.projectCount} projects.`,
    "",
    "Ask about clients, projects, statuses, or how to use DM OS.",
    "To enable full AI answers, set OPENAI_API_KEY and keep NEXT_PUBLIC_AI_COPILOT_ENABLED=true.",
  ].join("\n");
}

type ChatMessage = { role: "system" | "user" | "assistant"; content: string };

export async function generateOpenAiReply(params: {
  apiKey: string;
  messages: ChatMessage[];
}): Promise<string> {
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${params.apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: process.env.OPENAI_MODEL?.trim() || "gpt-4o-mini",
      temperature: 0.4,
      messages: params.messages,
    }),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(
      `OpenAI request failed (${response.status}): ${detail.slice(0, 200)}`,
    );
  }

  const data = (await response.json()) as {
    choices?: Array<{ message?: { content?: string } }>;
  };

  const content = data.choices?.[0]?.message?.content?.trim();
  if (!content) {
    throw new Error("OpenAI returned an empty response");
  }

  return content;
}
