import { z } from "zod";

export const clientStatuses = [
  "active",
  "inactive",
  "prospect",
] as const;

export const projectStatuses = [
  "planned",
  "active",
  "on_hold",
  "completed",
  "cancelled",
] as const;

export const clientSchema = z.object({
  name: z.string().trim().min(2, "Client name is required").max(120),
  email: z
    .string()
    .trim()
    .refine(
      (value) => value === "" || z.email().safeParse(value).success,
      "Enter a valid email",
    ),
  phone: z.string().trim().max(40),
  company: z.string().trim().max(500),
  status: z.enum(clientStatuses),
  notes: z.string().trim().max(2000),
});

export const projectSchema = z.object({
  clientId: z.string().uuid("Select a client"),
  name: z.string().trim().min(2, "Project name is required").max(120),
  description: z.string().trim().max(2000),
  status: z.enum(projectStatuses),
  dueDate: z
    .string()
    .refine(
      (value) => value === "" || /^\d{4}-\d{2}-\d{2}$/.test(value),
      "Use a valid date",
    ),
});

export type ClientInput = z.infer<typeof clientSchema>;
export type ProjectInput = z.infer<typeof projectSchema>;

export function toNullable(value: string) {
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : null;
}
