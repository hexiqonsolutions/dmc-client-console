import { redirect } from "next/navigation";

import { DashboardShell } from "@/components/layout/dashboard-shell";
import {
  isAiCopilotEnabled,
  isOpenAiConfigured,
  isSupabaseConfigured,
} from "@/lib/env";
import { requireWorkspace } from "@/lib/workspace";

export const dynamic = "force-dynamic";

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  if (!isSupabaseConfigured()) {
    redirect("/setup");
  }

  // Provisions a workspace if signup happened before SQL migrations.
  const workspace = await requireWorkspace();

  return (
    <DashboardShell
      fullName={workspace.profile?.full_name}
      email={workspace.email}
      role={workspace.role}
      organizationName={workspace.organization.name}
      organizationSlug={workspace.organization.slug}
      aiEnabled={isAiCopilotEnabled()}
      openAiConfigured={isOpenAiConfigured()}
    >
      {children}
    </DashboardShell>
  );
}
