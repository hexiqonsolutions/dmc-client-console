import Link from "next/link";
import {
  LayoutDashboard,
  Settings,
  Users,
  FolderKanban,
} from "lucide-react";

import { cn } from "@/lib/utils";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/dashboard/clients", label: "Clients", icon: Users, disabled: true },
  {
    href: "/dashboard/projects",
    label: "Projects",
    icon: FolderKanban,
    disabled: true,
  },
  {
    href: "/dashboard/settings",
    label: "Settings",
    icon: Settings,
    disabled: true,
  },
];

export function DashboardSidebar({
  organizationName,
}: {
  organizationName?: string | null;
}) {
  return (
    <aside className="flex w-60 shrink-0 flex-col border-r border-sidebar-border bg-sidebar text-sidebar-foreground">
      <div className="flex items-center gap-3 border-b border-sidebar-border px-4 py-4">
        <div className="flex size-9 items-center justify-center rounded-md bg-sidebar-accent text-sm font-semibold">
          <span className="text-sidebar-primary">DM</span>
        </div>
        <div className="min-w-0">
          <p className="truncate font-heading text-sm font-semibold tracking-tight">
            DM OS
          </p>
          <p className="truncate text-xs text-sidebar-foreground/70">
            {organizationName ?? "Workspace"}
          </p>
        </div>
      </div>

      <nav className="flex flex-1 flex-col gap-1 p-3" aria-label="Main">
        {navItems.map((item) => {
          const Icon = item.icon;
          if (item.disabled) {
            return (
              <span
                key={item.href}
                className={cn(
                  "flex cursor-not-allowed items-center gap-2 rounded-md px-3 py-2 text-sm text-sidebar-foreground/40",
                )}
                title="Coming in a later milestone"
              >
                <Icon className="size-4" aria-hidden />
                {item.label}
              </span>
            );
          }

          return (
            <Link
              key={item.href}
              href={item.href}
              className="flex items-center gap-2 rounded-md px-3 py-2 text-sm text-sidebar-foreground transition-colors hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
            >
              <Icon className="size-4" aria-hidden />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
