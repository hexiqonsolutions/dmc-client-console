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

export default function SetupPage() {
  const configured = isSupabaseConfigured();

  return (
    <div className="mx-auto flex min-h-full w-full max-w-2xl flex-col gap-6 px-6 py-12">
      <div className="space-y-2">
        <p className="text-sm font-medium text-primary">Milestone 2</p>
        <h1 className="text-3xl font-semibold tracking-tight">
          Connect Supabase
        </h1>
        <p className="text-muted-foreground">
          Auth and organizations need a Supabase project. Follow these steps
          once, then sign up.
        </p>
      </div>

      {configured ? (
        <Alert>
          <AlertTitle>Supabase keys detected</AlertTitle>
          <AlertDescription>
            Environment variables look set. If SQL is applied, you can{" "}
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
              Copy Project URL and anon public key into `.env.local` (from
              `.env.example`).
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
              <Link href="/signup">Go to sign up</Link>
            </Button>
            <Button asChild variant="outline" className="cursor-pointer">
              <Link href="/">Back home</Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
