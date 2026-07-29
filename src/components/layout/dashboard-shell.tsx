"use client";

import { useState } from "react";

import { CopilotRail } from "@/components/ai/copilot-rail";
import { DashboardSidebar } from "@/components/layout/dashboard-sidebar";
import { DashboardTopbar } from "@/components/layout/dashboard-topbar";

type DashboardShellProps = {
  children: React.ReactNode;
  fullName?: string | null;
  email?: string | null;
  role?: string | null;
  organizationName?: string | null;
  organizationSlug?: string | null;
  aiEnabled: boolean;
  openAiConfigured: boolean;
};

export function DashboardShell({
  children,
  fullName,
  email,
  role,
  organizationName,
  organizationSlug,
  aiEnabled,
  openAiConfigured,
}: DashboardShellProps) {
  const [copilotOpen, setCopilotOpen] = useState(aiEnabled);

  return (
    <div className="flex min-h-full flex-1">
      <div className="hidden md:flex">
        <DashboardSidebar organizationName={organizationName} />
      </div>
      <div className="flex min-w-0 flex-1 flex-col">
        <DashboardTopbar
          fullName={fullName}
          email={email}
          role={role}
          organizationName={organizationName}
          organizationSlug={organizationSlug}
          aiEnabled={aiEnabled}
          copilotOpen={copilotOpen}
          onToggleCopilot={() => setCopilotOpen((value) => !value)}
        />
        <div className="flex min-h-0 flex-1">
          <main className="min-w-0 flex-1 overflow-y-auto px-4 py-6 sm:px-6 sm:py-8">
            {children}
          </main>
          {aiEnabled ? (
            <div
              className={
                copilotOpen
                  ? "fixed inset-y-0 right-0 z-30 flex w-[min(100%,24rem)] shadow-lg md:static md:z-auto md:shadow-none"
                  : "hidden"
              }
            >
              <CopilotRail
                open={copilotOpen}
                onClose={() => setCopilotOpen(false)}
                openAiConfigured={openAiConfigured}
              />
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
