"use client";

import { Menu } from "lucide-react";

import { DashboardSidebar } from "@/components/layout/dashboard-sidebar";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

export function MobileSidebarTrigger({
  organizationName,
}: {
  organizationName?: string | null;
}) {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button
          type="button"
          variant="outline"
          size="icon"
          className="cursor-pointer md:hidden"
          aria-label="Open navigation"
        >
          <Menu className="size-4" />
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-60 border-sidebar-border bg-sidebar p-0 text-sidebar-foreground">
        <SheetHeader className="sr-only">
          <SheetTitle>Navigation</SheetTitle>
        </SheetHeader>
        <DashboardSidebar
          organizationName={organizationName}
          className="h-full w-full border-0"
        />
      </SheetContent>
    </Sheet>
  );
}
