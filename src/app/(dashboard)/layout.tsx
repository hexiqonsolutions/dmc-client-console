import { redirect } from "next/navigation";

import { DashboardSidebar } from "@/components/layout/dashboard-sidebar";
import { DashboardTopbar } from "@/components/layout/dashboard-topbar";
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
      <div className="hidden md:flex">
        <DashboardSidebar organizationName={workspace.organization?.name} />
      </div>
      <div className="flex min-w-0 flex-1 flex-col">
        <DashboardTopbar
          fullName={workspace.profile?.full_name}
          email={workspace.email}
          role={workspace.role}
          organizationName={workspace.organization?.name}
          organizationSlug={workspace.organization?.slug}
        />
        <main className="flex-1 px-4 py-6 sm:px-6 sm:py-8">{children}</main>
      </div>
    </div>
  );
}
