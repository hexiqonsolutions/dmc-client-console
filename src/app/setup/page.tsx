import type { Metadata } from "next";
import Link from "next/link";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { isSupabaseConfigured } from "@/lib/env";

export const metadata: Metadata = {
  title: "Setup",
};

type SetupPageProps = {
  searchParams?: Promise<{ reason?: string; error?: string }>;
};

export default async function SetupPage({ searchParams }: SetupPageProps) {
  const configured = isSupabaseConfigured();
  const params = searchParams ? await searchParams : {};
  const noOrganization = params.reason === "no-organization";

  return (
    <div className="mx-auto flex min-h-full w-full max-w-2xl flex-col gap-6 px-6 py-12">
      <div className="space-y-2">
        <p className="text-sm font-medium text-primary">Setup</p>
        <h1 className="text-3xl font-semibold tracking-tight">
          Connect Supabase
        </h1>
        <p className="text-muted-foreground">
          Auth and organizations need a Supabase project. Follow these steps
          once, then use the dashboard.
        </p>
      </div>

      {noOrganization ? (
        <Alert variant="destructive">
          <AlertTitle>Workspace not found for your account</AlertTitle>
          <AlertDescription>
            You are signed in, but no organization was created (usually because
            SQL migration 00001 ran after signup, or the service role key is
            missing). Confirm all 3 SQL migrations are applied, ensure
            `SUPABASE_SERVICE_ROLE_KEY` is in `.env.local`, restart the app, then
            open{" "}
            <Link
              href="/dashboard/clients"
              className="font-medium text-primary underline"
            >
              Clients
            </Link>{" "}
            again.{" "}
            {params.error ? (
              <span className="mt-2 block font-mono text-xs">{params.error}</span>
            ) : null}
          </AlertDescription>
        </Alert>
      ) : null}

      {configured ? (
        <Alert>
          <AlertTitle>Supabase keys detected</AlertTitle>
          <AlertDescription>
            Environment variables look set. If SQL is applied, open the{" "}
            <Link
              href="/dashboard"
              className="font-medium text-primary underline"
            >
              dashboard
            </Link>{" "}
            or{" "}
            <Link href="/signup" className="font-medium text-primary underline">
              create an account
            </Link>
            .
          </AlertDescription>
        </Alert>
      ) : (
        <Alert variant="destructive">
          <AlertTitle>Keys missing</AlertTitle>
          <AlertDescription>
            Add `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`
            to `.env.local`, then restart `npm run dev`.
          </AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Setup checklist</CardTitle>
          <CardDescription>
            Detailed guide: docs/installation.md and docs/database-schema.md
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4 text-sm text-muted-foreground">
          <ol className="list-decimal space-y-3 pl-5">
            <li>
              Create a project at{" "}
              <a
                className="font-medium text-primary underline"
                href="https://supabase.com"
                target="_blank"
                rel="noreferrer"
              >
                supabase.com
              </a>
            </li>
            <li>
              Copy Project URL, anon key, and service role key into `.env.local`.
            </li>
            <li>
              In Supabase → Authentication → URL Configuration, set Site URL to
              `http://localhost:3000` and add redirect{" "}
              `http://localhost:3000/auth/callback`.
            </li>
            <li>
              For local testing, disable “Confirm email” under Authentication →
              Providers → Email (optional but easier).
            </li>
            <li>
              Run SQL migrations in order in the SQL Editor:
              `00001_init_auth_orgs.sql`, `00002_clients_projects.sql`, then
              `00003_ai_copilot.sql`.
            </li>
            <li>Restart the Next.js dev server.</li>
          </ol>
          <div className="flex flex-wrap gap-3 pt-2">
            <Button asChild className="cursor-pointer">
              <Link href="/dashboard/clients">Retry Clients</Link>
            </Button>
            <Button asChild variant="outline" className="cursor-pointer">
              <Link href="/dashboard">Dashboard</Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
