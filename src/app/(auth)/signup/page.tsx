import type { Metadata } from "next";

import { AuthShell } from "@/components/auth/auth-shell";
import { SignupForm } from "@/components/auth/signup-form";

export const metadata: Metadata = {
  title: "Create account",
};

export default function SignupPage() {
  return (
    <AuthShell
      title="Create your workspace"
      description="Sign up once — we create your profile and organization automatically."
    >
      <SignupForm />
    </AuthShell>
  );
}
