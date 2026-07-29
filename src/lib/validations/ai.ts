import { z } from "zod";

export const copilotAskSchema = z.object({
  conversationId: z.string().uuid().nullable().optional(),
  message: z
    .string()
    .trim()
    .min(2, "Ask a short question")
    .max(2000, "Keep questions under 2000 characters"),
});

export type CopilotAskInput = z.infer<typeof copilotAskSchema>;
