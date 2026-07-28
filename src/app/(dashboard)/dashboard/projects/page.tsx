import type { Metadata } from "next";
import { FolderKanban } from "lucide-react";

import { EmptyState } from "@/components/shared/empty-state";
import { PageHeader } from "@/components/shared/page-header";
import { Badge } from "@/components/ui/badge";

export const metadata: Metadata = {
  title: "Projects",
};

export default function ProjectsPage() {
  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-8">
      <PageHeader
        badge={<Badge variant="outline">Coming in Milestone 4</Badge>}
        title="Projects"
        description="Track delivery work tied to each client. Full stack arrives in Milestone 4."
      />
      <EmptyState
        icon={FolderKanban}
        title="No projects yet"
        description="Project lists, statuses, and due dates will use the same empty and loading patterns you see here."
      />
    </div>
  );
}
