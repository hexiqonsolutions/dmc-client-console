import { Badge } from "@/components/ui/badge";
import type { ClientStatus, ProjectStatus } from "@/types/database";
import { cn } from "@/lib/utils";

const clientStatusStyles: Record<ClientStatus, string> = {
  active: "border-primary/30 bg-accent text-accent-foreground",
  prospect: "border-border bg-secondary text-secondary-foreground",
  inactive: "border-border bg-muted text-muted-foreground",
};

const projectStatusStyles: Record<ProjectStatus, string> = {
  planned: "border-border bg-secondary text-secondary-foreground",
  active: "border-primary/30 bg-accent text-accent-foreground",
  on_hold: "border-border bg-muted text-muted-foreground",
  completed: "border-border bg-secondary text-secondary-foreground",
  cancelled: "border-destructive/20 bg-destructive/10 text-destructive",
};

export function ClientStatusBadge({ status }: { status: ClientStatus }) {
  return (
    <Badge
      variant="outline"
      className={cn("capitalize", clientStatusStyles[status])}
    >
      {status}
    </Badge>
  );
}

export function ProjectStatusBadge({ status }: { status: ProjectStatus }) {
  return (
    <Badge
      variant="outline"
      className={cn("capitalize", projectStatusStyles[status])}
    >
      {status.replaceAll("_", " ")}
    </Badge>
  );
}
