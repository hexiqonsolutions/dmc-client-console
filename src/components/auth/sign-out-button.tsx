"use client";

import { useTransition } from "react";

import { signOutAction } from "@/app/actions/auth";
import { Button } from "@/components/ui/button";

export function SignOutButton() {
  const [isPending, startTransition] = useTransition();

  return (
    <Button
      type="button"
      variant="outline"
      className="cursor-pointer"
      disabled={isPending}
      onClick={() => startTransition(() => signOutAction())}
    >
      {isPending ? "Signing out…" : "Sign out"}
    </Button>
  );
}
