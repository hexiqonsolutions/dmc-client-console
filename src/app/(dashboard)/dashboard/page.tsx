import type { Metadata } from "next";
import Link from "next/link";

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
    <div className="mx-auto flex w-full max-w-4xl flex-col gap-8">
      <section className="space-y-3">
        <Badge variant="secondary">Milestone 2</Badge>
        <h1 className="text-3xl font-semibold tracking-tight">
          Welcome{workspace?.profile?.full_name ? `, ${workspace.profile.full_name}` : ""}
        </h1>
        <p className="max-w-2xl text-muted-foreground">
          Auth and your organization workspace are live. Clients and projects
          arrive in Milestone 4 after the app shell polish in Milestone 3.
        </p>
      </section>

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
                  {workspace.role}
                </p>
              </>
            ) : (
              <div className="space-y-3">
                <p className="text-muted-foreground">
                  No organization found. Confirm the SQL migration ran after
                  signup.
                </p>
                <Button asChild variant="outline" className="cursor-pointer">
                  <Link href="/setup">Open setup guide</Link>
                </Button>
              </div>
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
              <span className="font-mono text-xs">{workspace?.userId}</span>
            </p>
          </CardContent>
        </Card>
      </section>

      <Card>
        <CardHeader>
          <CardTitle>Empty modules</CardTitle>
          <CardDescription>
            Placeholder areas for upcoming milestones
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="rounded-lg border border-dashed border-border bg-muted/40 px-6 py-10 text-center">
            <p className="text-sm font-medium text-foreground">
              No clients or projects yet
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              Milestone 4 adds full CRUD for clients and projects.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
