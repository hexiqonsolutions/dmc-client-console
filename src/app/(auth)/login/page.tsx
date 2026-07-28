import type { Metadata } from "next";
import { Suspense } from "react";

import { AuthShell } from "@/components/auth/auth-shell";
import { LoginForm } from "@/components/auth/login-form";

export const metadata: Metadata = {
  title: "Sign in",
};

export default function LoginPage() {
  return (
    <AuthShell
      title="Sign in to DM OS"
      description="Access your agency workspace, clients, and projects."
    >
      <Suspense
        fallback={
          <p className="text-sm text-muted-foreground">Loading sign-in…</p>
        }
      >
        <LoginForm />
      </Suspense>
    </AuthShell>
  );
}
