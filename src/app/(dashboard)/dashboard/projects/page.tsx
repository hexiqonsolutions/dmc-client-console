import type { Metadata } from "next";

import { ProjectsPanel } from "@/components/crm/projects-panel";
import { ErrorState } from "@/components/shared/error-state";
import { PageHeader } from "@/components/shared/page-header";
import { Badge } from "@/components/ui/badge";
import { listClients, listProjects } from "@/lib/data/crm";
import { requireWorkspace } from "@/lib/workspace";
import type { Client, ProjectWithClient } from "@/types/database";

export const metadata: Metadata = {
  title: "Projects",
};

export default async function ProjectsPage() {
  const workspace = await requireWorkspace();

  let clients: Client[] = [];
  let projects: ProjectWithClient[] = [];
  let loadError: string | null = null;

  try {
    [clients, projects] = await Promise.all([
      listClients(workspace.organization.id),
      listProjects(workspace.organization.id),
    ]);
  } catch (error) {
    loadError =
      error instanceof Error
        ? error.message
        : "Could not load projects. Run the Milestone 4 SQL migration.";
  }

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-8">
      <PageHeader
        badge={<Badge variant="secondary">Milestone 4</Badge>}
        title="Projects"
        description="Track delivery work tied to each client in your workspace."
      />

      {loadError ? (
        <ErrorState
          title="Projects unavailable"
          description={`${loadError} Apply supabase/migrations/00002_clients_projects.sql in the Supabase SQL Editor, then refresh.`}
          retryHref="/dashboard/projects"
        />
      ) : (
        <ProjectsPanel projects={projects} clients={clients} />
      )}
    </div>
  );
}
