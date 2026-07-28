import { SignOutButton } from "@/components/auth/sign-out-button";
import { MobileSidebarTrigger } from "@/components/layout/mobile-sidebar-trigger";
import { Badge } from "@/components/ui/badge";

type DashboardTopbarProps = {
  fullName?: string | null;
  email?: string | null;
  role?: string | null;
  organizationName?: string | null;
  organizationSlug?: string | null;
};

export function DashboardTopbar({
  fullName,
  email,
  role,
  organizationName,
  organizationSlug,
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
      <SignOutButton />
    </header>
  );
}
