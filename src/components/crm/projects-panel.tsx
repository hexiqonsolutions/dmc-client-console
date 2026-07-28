"use client";

import {
  FolderKanban,
  MoreHorizontal,
  Pencil,
  Plus,
  Trash2,
} from "lucide-react";
import { useMemo, useState } from "react";

import { deleteProjectAction } from "@/app/actions/projects";
import { ConfirmDeleteDialog } from "@/components/crm/confirm-delete-dialog";
import { ProjectFormDialog } from "@/components/crm/project-form-dialog";
import { ProjectStatusBadge } from "@/components/crm/status-badges";
import { EmptyState } from "@/components/shared/empty-state";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { Client, ProjectWithClient } from "@/types/database";

export function ProjectsPanel({
  projects,
  clients,
}: {
  projects: ProjectWithClient[];
  clients: Client[];
}) {
  const [query, setQuery] = useState("");
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<ProjectWithClient | null>(null);
  const [deleting, setDeleting] = useState<ProjectWithClient | null>(null);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) {
      return projects;
    }
    return projects.filter((project) =>
      [project.name, project.clients?.name, project.status]
        .filter(Boolean)
        .some((value) => String(value).toLowerCase().includes(q)),
    );
  }, [projects, query]);

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <Input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search projects…"
          className="max-w-sm"
          aria-label="Search projects"
        />
        <Button
          type="button"
          className="cursor-pointer"
          disabled={clients.length === 0}
          onClick={() => {
            setEditing(null);
            setFormOpen(true);
          }}
        >
          <Plus className="size-4" />
          Add project
        </Button>
      </div>

      {clients.length === 0 ? (
        <EmptyState
          icon={FolderKanban}
          title="Add a client first"
          description="Projects must belong to a client. Create a client, then come back here."
          actionLabel="Go to clients"
          actionHref="/dashboard/clients"
        />
      ) : projects.length === 0 ? (
        <EmptyState
          icon={FolderKanban}
          title="No projects yet"
          description="Create a project to track delivery for one of your clients."
          actionLabel="Add project"
          onAction={() => {
            setEditing(null);
            setFormOpen(true);
          }}
        />
      ) : filtered.length === 0 ? (
        <EmptyState
          icon={FolderKanban}
          title="No matches"
          description="Try a different search term."
        />
      ) : (
        <div className="overflow-hidden rounded-xl border border-border bg-card">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Project</TableHead>
                <TableHead>Client</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Due</TableHead>
                <TableHead className="w-12">
                  <span className="sr-only">Actions</span>
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map((project) => (
                <TableRow key={project.id}>
                  <TableCell className="font-medium">{project.name}</TableCell>
                  <TableCell>{project.clients?.name ?? "—"}</TableCell>
                  <TableCell>
                    <ProjectStatusBadge status={project.status} />
                  </TableCell>
                  <TableCell>
                    {project.due_date
                      ? new Date(project.due_date).toLocaleDateString()
                      : "—"}
                  </TableCell>
                  <TableCell>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button
                          type="button"
                          variant="ghost"
                          size="icon"
                          className="cursor-pointer"
                          aria-label={`Actions for ${project.name}`}
                        >
                          <MoreHorizontal className="size-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem
                          className="cursor-pointer"
                          onClick={() => {
                            setEditing(project);
                            setFormOpen(true);
                          }}
                        >
                          <Pencil className="size-4" />
                          Edit
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          className="cursor-pointer text-destructive focus:text-destructive"
                          onClick={() => setDeleting(project)}
                        >
                          <Trash2 className="size-4" />
                          Delete
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}

      <ProjectFormDialog
        open={formOpen}
        onOpenChange={setFormOpen}
        clients={clients}
        project={editing}
      />

      <ConfirmDeleteDialog
        open={Boolean(deleting)}
        onOpenChange={(open) => {
          if (!open) {
            setDeleting(null);
          }
        }}
        title="Delete project?"
        description={
          deleting
            ? `This permanently deletes “${deleting.name}”.`
            : ""
        }
        onConfirm={async () => {
          if (!deleting) {
            return { success: false, error: "No project selected" };
          }
          return deleteProjectAction(deleting.id);
        }}
      />
    </div>
  );
}
