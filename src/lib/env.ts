/**
 * Env helpers for DM OS.
 * Public Supabase keys are required from Milestone 2 onward.
 */

export function isSupabaseConfigured(): boolean {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY?.trim();
  return Boolean(url && anonKey);
}

export function getSupabaseEnv() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY?.trim();

  if (!url || !anonKey) {
    throw new Error(
      "Missing NEXT_PUBLIC_SUPABASE_URL or NEXT_PUBLIC_SUPABASE_ANON_KEY. See docs/installation.md.",
    );
  }

  return { url, anonKey };
}

export function getAppUrl() {
  return (
    process.env.NEXT_PUBLIC_APP_URL?.trim() || "http://localhost:3000"
  ).replace(/\/$/, "");
}

/** Milestone 5 — show Copilot rail when enabled (default off). */
export function isAiCopilotEnabled(): boolean {
  const value = process.env.NEXT_PUBLIC_AI_COPILOT_ENABLED?.trim().toLowerCase();
  return value === "true" || value === "1" || value === "yes";
}

export function getOpenAiApiKey() {
  return process.env.OPENAI_API_KEY?.trim() || null;
}

export function isOpenAiConfigured(): boolean {
  return Boolean(getOpenAiApiKey());
}
