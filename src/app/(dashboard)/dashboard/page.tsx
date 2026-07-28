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
import { getWorkspaceContext } from "@/lib/workspace";

export const metadata: Metadata = {
  title: "Dashboard",
};

export default async function DashboardPage() {
  const workspace = await getWorkspaceContext();

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-8">
      <PageHeader
        badge={<Badge variant="secondary">Milestone 3</Badge>}
        title={`Welcome${workspace?.profile?.full_name ? `, ${workspace.profile.full_name}` : ""}`}
        description="Your app shell is ready — active navigation, branded logo, and shared empty/loading patterns for every module."
        actions={
          <Button asChild variant="outline" className="cursor-pointer">
            <Link href="/dashboard/clients">Browse clients</Link>
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
            <CardTitle>Account</CardTitle>
            <CardDescription>Signed-in identity</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            <p>
              <span className="text-muted-foreground">Email: </span>
              {workspace?.email ?? "—"}
            </p>
            <p>
              <span className="text-muted-foreground">User ID: </span>
              <span className="break-all font-mono text-xs">
                {workspace?.userId}
              </span>
            </p>
          </CardContent>
        </Card>
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        <EmptyState
          icon={Users}
          title="No clients yet"
          description="Client CRM arrives in Milestone 4. The empty state pattern is ready now."
          actionLabel="Open clients"
          actionHref="/dashboard/clients"
        />
        <EmptyState
          icon={FolderKanban}
          title="No projects yet"
          description="Projects will connect to clients in Milestone 4."
          actionLabel="Open projects"
          actionHref="/dashboard/projects"
        />
      </section>
    </div>
  );
}
