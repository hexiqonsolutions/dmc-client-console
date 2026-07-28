import type { Metadata } from "next";
import { Settings } from "lucide-react";

import { EmptyState } from "@/components/shared/empty-state";
import { PageHeader } from "@/components/shared/page-header";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { getWorkspaceContext } from "@/lib/workspace";

export const metadata: Metadata = {
  title: "Settings",
};

export default async function SettingsPage() {
  const workspace = await getWorkspaceContext();

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-8">
      <PageHeader
        badge={<Badge variant="secondary">Workspace</Badge>}
        title="Settings"
        description="Organization profile and team settings expand in later milestones."
      />

      <Card>
        <CardHeader>
          <CardTitle>Organization</CardTitle>
          <CardDescription>Read-only view for Milestone 3</CardDescription>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <p>
            <span className="text-muted-foreground">Name: </span>
            {workspace?.organization?.name ?? "—"}
          </p>
          <p>
            <span className="text-muted-foreground">Slug: </span>
            <span className="font-mono text-xs">
              {workspace?.organization?.slug ?? "—"}
            </span>
          </p>
          <p>
            <span className="text-muted-foreground">Your role: </span>
            <span className="capitalize">{workspace?.role ?? "—"}</span>
          </p>
        </CardContent>
      </Card>

      <EmptyState
        icon={Settings}
        title="More settings soon"
        description="Team invites, billing, and brand preferences will appear here without inventing new layout patterns."
      />
    </div>
  );
}
