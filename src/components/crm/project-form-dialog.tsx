"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useTransition } from "react";
import { Controller, useForm } from "react-hook-form";
import { toast } from "sonner";

import {
  createProjectAction,
  updateProjectAction,
} from "@/app/actions/projects";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import {
  projectSchema,
  projectStatuses,
  type ProjectInput,
} from "@/lib/validations/crm";
import type { Client, ProjectWithClient } from "@/types/database";

type ProjectFormDialogProps = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  clients: Client[];
  project?: ProjectWithClient | null;
};

export function ProjectFormDialog({
  open,
  onOpenChange,
  clients,
  project,
}: ProjectFormDialogProps) {
  const [isPending, startTransition] = useTransition();
  const isEditing = Boolean(project);

  const form = useForm<ProjectInput>({
    resolver: zodResolver(projectSchema),
    defaultValues: {
      clientId: "",
      name: "",
      description: "",
      status: "planned",
      dueDate: "",
    },
  });

  useEffect(() => {
    if (!open) {
      return;
    }

    form.reset({
      clientId: project?.client_id ?? clients[0]?.id ?? "",
      name: project?.name ?? "",
      description: project?.description ?? "",
      status: project?.status ?? "planned",
      dueDate: project?.due_date ?? "",
    });
  }, [clients, form, open, project]);

  function onSubmit(values: ProjectInput) {
    startTransition(async () => {
      const result = project
        ? await updateProjectAction(project.id, values)
        : await createProjectAction(values);

      if (!result.success) {
        toast.error(result.error);
        return;
      }

      toast.success(result.message ?? "Saved");
      onOpenChange(false);
    });
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-lg" showCloseButton={!isPending}>
        <DialogHeader>
          <DialogTitle>
            {isEditing ? "Edit project" : "Add project"}
          </DialogTitle>
          <DialogDescription>
            Every project must belong to a client in your workspace.
          </DialogDescription>
        </DialogHeader>

        {clients.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Add a client first, then create projects for them.
          </p>
        ) : (
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="space-y-4"
            noValidate
          >
            <div className="space-y-2">
              <Label>Client</Label>
              <Controller
                control={form.control}
                name="clientId"
                render={({ field }) => (
                  <Select
                    value={field.value}
                    onValueChange={field.onChange}
                    disabled={isPending}
                  >
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Select client" />
                    </SelectTrigger>
                    <SelectContent>
                      {clients.map((client) => (
                        <SelectItem key={client.id} value={client.id}>
                          {client.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
              {form.formState.errors.clientId ? (
                <p className="text-sm text-destructive">
                  {form.formState.errors.clientId.message}
                </p>
              ) : null}
            </div>

            <div className="space-y-2">
              <Label htmlFor="project-name">Project name</Label>
              <Input
                id="project-name"
                disabled={isPending}
                {...form.register("name")}
              />
              {form.formState.errors.name ? (
                <p className="text-sm text-destructive">
                  {form.formState.errors.name.message}
                </p>
              ) : null}
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label>Status</Label>
                <Controller
                  control={form.control}
                  name="status"
                  render={({ field }) => (
                    <Select
                      value={field.value}
                      onValueChange={field.onChange}
                      disabled={isPending}
                    >
                      <SelectTrigger className="w-full">
                        <SelectValue placeholder="Select status" />
                      </SelectTrigger>
                      <SelectContent>
                        {projectStatuses.map((status) => (
                          <SelectItem key={status} value={status}>
                            <span className="capitalize">
                              {status.replaceAll("_", " ")}
                            </span>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  )}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="project-due">Due date</Label>
                <Input
                  id="project-due"
                  type="date"
                  disabled={isPending}
                  {...form.register("dueDate")}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="project-description">Description</Label>
              <Textarea
                id="project-description"
                rows={3}
                disabled={isPending}
                {...form.register("description")}
              />
            </div>

            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                className="cursor-pointer"
                disabled={isPending}
                onClick={() => onOpenChange(false)}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                className="cursor-pointer"
                disabled={isPending}
              >
                {isPending
                  ? "Saving…"
                  : isEditing
                    ? "Save changes"
                    : "Create project"}
              </Button>
            </DialogFooter>
          </form>
        )}
      </DialogContent>
    </Dialog>
  );
}
