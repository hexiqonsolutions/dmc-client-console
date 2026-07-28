"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  FolderKanban,
  LayoutDashboard,
  Settings,
  Users,
  type LucideIcon,
} from "lucide-react";

import { BrandLogo } from "@/components/brand/brand-logo";
import { dashboardNav, isNavActive } from "@/lib/navigation";
import { cn } from "@/lib/utils";

const icons: Record<string, LucideIcon> = {
  "/dashboard": LayoutDashboard,
  "/dashboard/clients": Users,
  "/dashboard/projects": FolderKanban,
  "/dashboard/settings": Settings,
};

export function DashboardSidebar({
  organizationName,
  className,
}: {
  organizationName?: string | null;
  className?: string;
}) {
  const pathname = usePathname();

  return (
    <aside
      className={cn(
        "flex h-full w-60 shrink-0 flex-col border-r border-sidebar-border bg-sidebar text-sidebar-foreground",
        className,
      )}
    >
      <div className="border-b border-sidebar-border px-4 py-4">
        <BrandLogo
          href="/dashboard"
          onDark
          subtitle={organizationName ?? "Workspace"}
        />
      </div>

      <nav className="flex flex-1 flex-col gap-1 p-3" aria-label="Main">
        {dashboardNav.map((item) => {
          const Icon = icons[item.href] ?? LayoutDashboard;
          const active = isNavActive(pathname, item.href, item.exact);

          return (
            <Link
              key={item.href}
              href={item.href}
              aria-current={active ? "page" : undefined}
              className={cn(
                "flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors duration-200",
                active
                  ? "bg-sidebar-accent font-medium text-sidebar-accent-foreground"
                  : "text-sidebar-foreground/80 hover:bg-sidebar-accent/80 hover:text-sidebar-accent-foreground",
              )}
            >
              <Icon className="size-4 shrink-0" aria-hidden />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-sidebar-border p-4">
        <p className="text-xs text-sidebar-foreground/50">
          DM Creatives Operating System
        </p>
      </div>
    </aside>
  );
}
