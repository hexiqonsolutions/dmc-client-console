"use client";

import { Sparkles } from "lucide-react";

import { SignOutButton } from "@/components/auth/sign-out-button";
import { MobileSidebarTrigger } from "@/components/layout/mobile-sidebar-trigger";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

type DashboardTopbarProps = {
  fullName?: string | null;
  email?: string | null;
  role?: string | null;
  organizationName?: string | null;
  organizationSlug?: string | null;
  aiEnabled?: boolean;
  copilotOpen?: boolean;
  onToggleCopilot?: () => void;
};

export function DashboardTopbar({
  fullName,
  email,
  role,
  organizationName,
  organizationSlug,
  aiEnabled = false,
  copilotOpen = false,
  onToggleCopilot,
}: DashboardTopbarProps) {
  return (
    <header className="sticky top-0 z-20 flex items-center justify-between gap-4 border-b border-border/80 bg-card/90 px-4 py-3 backdrop-blur-sm sm:px-6">
      <div className="flex min-w-0 items-center gap-3">
        <MobileSidebarTrigger organizationName={organizationName} />
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <p className="truncate text-sm font-medium text-foreground">
              {fullName || email || "Account"}
            </p>
            {role ? (
              <Badge variant="secondary" className="capitalize">
                {role}
              </Badge>
            ) : null}
          </div>
          <p className="truncate text-xs text-muted-foreground">
            {organizationName ?? "No organization"}
            {organizationSlug ? (
              <span className="font-mono"> · {organizationSlug}</span>
            ) : null}
          </p>
        </div>
      </div>
      <div className="flex items-center gap-2">
        {aiEnabled && onToggleCopilot ? (
          <Button
            type="button"
            variant={copilotOpen ? "secondary" : "outline"}
            size="sm"
            className="cursor-pointer"
            onClick={onToggleCopilot}
            aria-pressed={copilotOpen}
          >
            <Sparkles className="size-4" />
            <span className="hidden sm:inline">Copilot</span>
          </Button>
        ) : null}
        <SignOutButton />
      </div>
    </header>
  );
}
