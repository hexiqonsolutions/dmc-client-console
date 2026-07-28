"use client";

import { MoreHorizontal, Pencil, Plus, Trash2 } from "lucide-react";
import { useMemo, useState } from "react";

import { deleteClientAction } from "@/app/actions/clients";
import { ClientFormDialog } from "@/components/crm/client-form-dialog";
import { ConfirmDeleteDialog } from "@/components/crm/confirm-delete-dialog";
import { ClientStatusBadge } from "@/components/crm/status-badges";
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
import type { Client } from "@/types/database";
import { Users } from "lucide-react";

export function ClientsPanel({ clients }: { clients: Client[] }) {
  const [query, setQuery] = useState("");
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<Client | null>(null);
  const [deleting, setDeleting] = useState<Client | null>(null);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) {
      return clients;
    }
    return clients.filter((client) =>
      [client.name, client.company, client.email, client.phone]
        .filter(Boolean)
        .some((value) => value!.toLowerCase().includes(q)),
    );
  }, [clients, query]);

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <Input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search clients…"
          className="max-w-sm"
          aria-label="Search clients"
        />
        <Button
          type="button"
          className="cursor-pointer"
          onClick={() => {
            setEditing(null);
            setFormOpen(true);
          }}
        >
          <Plus className="size-4" />
          Add client
        </Button>
      </div>

      {clients.length === 0 ? (
        <EmptyState
          icon={Users}
          title="No clients yet"
          description="Add your first client to start tracking agency relationships."
          actionLabel="Add client"
          onAction={() => {
            setEditing(null);
            setFormOpen(true);
          }}
        />
      ) : filtered.length === 0 ? (
        <EmptyState
          icon={Users}
          title="No matches"
          description="Try a different search term."
        />
      ) : (
        <div className="overflow-hidden rounded-xl border border-border bg-card">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Company</TableHead>
                <TableHead>Contact</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="w-12">
                  <span className="sr-only">Actions</span>
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map((client) => (
                <TableRow key={client.id}>
                  <TableCell className="font-medium">{client.name}</TableCell>
                  <TableCell>{client.company ?? "—"}</TableCell>
                  <TableCell>
                    <div className="space-y-0.5 text-sm">
                      <p>{client.email ?? "—"}</p>
                      <p className="text-muted-foreground">
                        {client.phone ?? "—"}
                      </p>
                    </div>
                  </TableCell>
                  <TableCell>
                    <ClientStatusBadge status={client.status} />
                  </TableCell>
                  <TableCell>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button
                          type="button"
                          variant="ghost"
                          size="icon"
                          className="cursor-pointer"
                          aria-label={`Actions for ${client.name}`}
                        >
                          <MoreHorizontal className="size-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem
                          className="cursor-pointer"
                          onClick={() => {
                            setEditing(client);
                            setFormOpen(true);
                          }}
                        >
                          <Pencil className="size-4" />
                          Edit
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          className="cursor-pointer text-destructive focus:text-destructive"
                          onClick={() => setDeleting(client)}
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

      <ClientFormDialog
        open={formOpen}
        onOpenChange={setFormOpen}
        client={editing}
      />

      <ConfirmDeleteDialog
        open={Boolean(deleting)}
        onOpenChange={(open) => {
          if (!open) {
            setDeleting(null);
          }
        }}
        title="Delete client?"
        description={
          deleting
            ? `This permanently deletes “${deleting.name}” and any related projects.`
            : ""
        }
        onConfirm={async () => {
          if (!deleting) {
            return { success: false, error: "No client selected" };
          }
          return deleteClientAction(deleting.id);
        }}
      />
    </div>
  );
}
