import type { Metadata } from "next";
import Link from "next/link";
import { FolderKanban, Users } from "lucide-react";

import { EmptyState } from "@/components/shared/empty-state";
import { PageHeader } from "@/components/shared/page-header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { listClients, listProjects } from "@/lib/data/crm";
import { getWorkspaceContext } from "@/lib/workspace";

export const metadata: Metadata = {
  title: "Dashboard",
};

export default async function DashboardPage() {
  const workspace = await getWorkspaceContext();

  let clientCount = 0;
  let projectCount = 0;
  let crmReady = true;

  if (workspace?.organization) {
    try {
      const [clients, projects] = await Promise.all([
        listClients(workspace.organization.id),
        listProjects(workspace.organization.id),
      ]);
      clientCount = clients.length;
      projectCount = projects.length;
    } catch {
      crmReady = false;
    }
  }

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-8">
      <PageHeader
        badge={<Badge variant="secondary">Milestone 4</Badge>}
        title={`Welcome${workspace?.profile?.full_name ? `, ${workspace.profile.full_name}` : ""}`}
        description="Clients and projects are live — add records, edit them, and keep delivery scoped to your organization."
        actions={
          <Button asChild className="cursor-pointer">
            <Link href="/dashboard/clients">Manage clients</Link>
          </Button>
        }
      />

      <section className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Workspace</CardTitle>
            <CardDescription>Your primary organization</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            {workspace?.organization ? (
              <>
                <p>
                  <span className="text-muted-foreground">Name: </span>
                  {workspace.organization.name}
                </p>
                <p>
                  <span className="text-muted-foreground">Slug: </span>
                  <span className="font-mono text-xs">
                    {workspace.organization.slug}
                  </span>
                </p>
                <p>
                  <span className="text-muted-foreground">Your role: </span>
                  <span className="capitalize">{workspace.role}</span>
                </p>
              </>
            ) : (
              <EmptyState
                className="border-0 bg-transparent px-0 py-6"
                title="No organization yet"
                description="Confirm the SQL migration ran, then create a new account."
                actionLabel="Open setup"
                actionHref="/setup"
              />
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>CRM snapshot</CardTitle>
            <CardDescription>Counts for this workspace</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            {crmReady ? (
              <>
                <p>
                  <span className="text-muted-foreground">Clients: </span>
                  {clientCount}
                </p>
                <p>
                  <span className="text-muted-foreground">Projects: </span>
                  {projectCount}
                </p>
              </>
            ) : (
              <p className="text-muted-foreground">
                Run `00002_clients_projects.sql` in Supabase to enable CRM
                tables.
              </p>
            )}
          </CardContent>
        </Card>
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        <EmptyState
          icon={Users}
          title={clientCount === 0 ? "No clients yet" : `${clientCount} clients`}
          description={
            clientCount === 0
              ? "Add your first client to unlock projects."
              : "Open the clients module to add, edit, or search."
          }
          actionLabel="Open clients"
          actionHref="/dashboard/clients"
        />
        <EmptyState
          icon={FolderKanban}
          title={
            projectCount === 0 ? "No projects yet" : `${projectCount} projects`
          }
          description={
            projectCount === 0
              ? "Create a project once you have at least one client."
              : "Track status and due dates in the projects module."
          }
          actionLabel="Open projects"
          actionHref="/dashboard/projects"
        />
      </section>
    </div>
  );
}
