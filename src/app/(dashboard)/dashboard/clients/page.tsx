import type { Metadata } from "next";

import { ClientsPanel } from "@/components/crm/clients-panel";
import { ErrorState } from "@/components/shared/error-state";
import { PageHeader } from "@/components/shared/page-header";
import { Badge } from "@/components/ui/badge";
import { listClients } from "@/lib/data/crm";
import { requireWorkspace } from "@/lib/workspace";
import type { Client } from "@/types/database";

export const metadata: Metadata = {
  title: "Clients",
};

export default async function ClientsPage() {
  const workspace = await requireWorkspace();

  let clients: Client[] = [];
  let loadError: string | null = null;

  try {
    clients = await listClients(workspace.organization.id);
  } catch (error) {
    loadError =
      error instanceof Error
        ? error.message
        : "Could not load clients. Run the Milestone 4 SQL migration.";
  }

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-8">
      <PageHeader
        badge={<Badge variant="secondary">Milestone 4</Badge>}
        title="Clients"
        description="Create and manage agency clients for your organization."
      />

      {loadError ? (
        <ErrorState
          title="Clients unavailable"
          description={`${loadError} Apply supabase/migrations/00002_clients_projects.sql in the Supabase SQL Editor, then refresh.`}
          retryHref="/dashboard/clients"
        />
      ) : (
        <ClientsPanel clients={clients} />
      )}
    </div>
  );
}
