import type { Metadata } from "next";
import { Users } from "lucide-react";

import { EmptyState } from "@/components/shared/empty-state";
import { PageHeader } from "@/components/shared/page-header";
import { Badge } from "@/components/ui/badge";

export const metadata: Metadata = {
  title: "Clients",
};

export default function ClientsPage() {
  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-8">
      <PageHeader
        badge={<Badge variant="outline">Coming in Milestone 4</Badge>}
        title="Clients"
        description="Manage agency clients in one place. CRUD, validation, and RLS land next."
      />
      <EmptyState
        icon={Users}
        title="No clients yet"
        description="When Milestone 4 ships, you will add, edit, and search clients scoped to your organization."
      />
    </div>
  );
}
