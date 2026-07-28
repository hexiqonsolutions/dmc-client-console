import { redirect } from "next/navigation";

import { SignOutButton } from "@/components/auth/sign-out-button";
import { DashboardSidebar } from "@/components/layout/dashboard-sidebar";
import { isSupabaseConfigured } from "@/lib/env";
import { getWorkspaceContext } from "@/lib/workspace";

export const dynamic = "force-dynamic";

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  if (!isSupabaseConfigured()) {
    redirect("/setup");
  }

  const workspace = await getWorkspaceContext();
  if (!workspace) {
    redirect("/login");
  }

  return (
    <div className="flex min-h-full flex-1">
      <DashboardSidebar organizationName={workspace.organization?.name} />
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex items-center justify-between border-b border-border/80 bg-card/80 px-6 py-3 backdrop-blur-sm">
          <div className="min-w-0">
            <p className="truncate text-sm font-medium text-foreground">
              {workspace.profile?.full_name ?? workspace.email}
            </p>
            <p className="truncate text-xs text-muted-foreground">
              {workspace.role ? `${workspace.role} · ` : null}
              {workspace.organization?.slug ?? "No organization yet"}
            </p>
          </div>
          <SignOutButton />
        </header>
        <main className="flex-1 px-6 py-8">{children}</main>
      </div>
    </div>
  );
}
