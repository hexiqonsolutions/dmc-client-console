"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useTransition } from "react";
import { Controller, useForm } from "react-hook-form";
import { toast } from "sonner";

import {
  createClientAction,
  updateClientAction,
} from "@/app/actions/clients";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
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
  clientSchema,
  clientStatuses,
  type ClientInput,
} from "@/lib/validations/crm";
import type { Client } from "@/types/database";

type ClientFormDialogProps = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  client?: Client | null;
};

export function ClientFormDialog({
  open,
  onOpenChange,
  client,
}: ClientFormDialogProps) {
  const [isPending, startTransition] = useTransition();
  const isEditing = Boolean(client);

  const form = useForm<ClientInput>({
    resolver: zodResolver(clientSchema),
    defaultValues: {
      name: "",
      email: "",
      phone: "",
      company: "",
      status: "active",
      notes: "",
    },
  });

  useEffect(() => {
    if (!open) {
      return;
    }

    form.reset({
      name: client?.name ?? "",
      email: client?.email ?? "",
      phone: client?.phone ?? "",
      company: client?.company ?? "",
      status: client?.status ?? "active",
      notes: client?.notes ?? "",
    });
  }, [client, form, open]);

  function onSubmit(values: ClientInput) {
    startTransition(async () => {
      const result = client
        ? await updateClientAction(client.id, values)
        : await createClientAction(values);

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
          <DialogTitle>{isEditing ? "Edit client" : "Add client"}</DialogTitle>
          <DialogDescription>
            Clients are scoped to your organization and protected by RLS.
          </DialogDescription>
        </DialogHeader>

        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="space-y-4"
          noValidate
        >
          {form.formState.errors.root ? (
            <Alert variant="destructive">
              <AlertTitle>Could not save</AlertTitle>
              <AlertDescription>
                {form.formState.errors.root.message}
              </AlertDescription>
            </Alert>
          ) : null}

          <div className="space-y-2">
            <Label htmlFor="client-name">Name</Label>
            <Input
              id="client-name"
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
              <Label htmlFor="client-email">Email</Label>
              <Input
                id="client-email"
                type="email"
                disabled={isPending}
                {...form.register("email")}
              />
              {form.formState.errors.email ? (
                <p className="text-sm text-destructive">
                  {form.formState.errors.email.message}
                </p>
              ) : null}
            </div>
            <div className="space-y-2">
              <Label htmlFor="client-phone">Phone</Label>
              <Input
                id="client-phone"
                disabled={isPending}
                {...form.register("phone")}
              />
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="client-company">Company</Label>
              <Input
                id="client-company"
                disabled={isPending}
                {...form.register("company")}
              />
            </div>
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
                      {clientStatuses.map((status) => (
                        <SelectItem key={status} value={status}>
                          <span className="capitalize">{status}</span>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="client-notes">Notes</Label>
            <Textarea
              id="client-notes"
              rows={3}
              disabled={isPending}
              {...form.register("notes")}
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
            <Button type="submit" className="cursor-pointer" disabled={isPending}>
              {isPending ? "Saving…" : isEditing ? "Save changes" : "Create client"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
