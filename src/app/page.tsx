import Link from "next/link";
import { CheckCircle2, Circle } from "lucide-react";

import { BrandLogo } from "@/components/brand/brand-logo";
import { TokenSwatch } from "@/components/foundation/token-swatch";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { isSupabaseConfigured } from "@/lib/env";

const foundationChecks = [
  { label: "Next.js App Router + TypeScript", done: true },
  { label: "Tailwind CSS v4 + shadcn/ui", done: true },
  { label: "Studio Command design tokens", done: true },
  { label: "Supabase auth + organizations", done: true },
  { label: "Protected /dashboard routes", done: true },
  { label: "App shell polish + brand assets", done: true },
  { label: "Clients + Projects CRUD", done: true },
  { label: "AI Copilot (Milestone 5)", done: false },
];

const tokens = [
  { name: "Primary", value: "#0F766E", className: "bg-primary" },
  { name: "Ink / Sidebar", value: "#0B1220", className: "bg-sidebar" },
  { name: "Background", value: "#F5F7FA", className: "bg-background" },
  { name: "Surface", value: "#FFFFFF", className: "bg-card" },
  { name: "CTA", value: "#C2410C", className: "bg-cta" },
  { name: "Muted text", value: "#64748B", className: "bg-muted-foreground" },
];

export default function HomePage() {
  const configured = isSupabaseConfigured();

  return (
    <div className="flex flex-1 flex-col">
      <header className="border-b border-border/80 bg-card/80 backdrop-blur-sm">
        <div className="mx-auto flex w-full max-w-5xl items-center justify-between gap-4 px-6 py-4">
          <BrandLogo
            href="/"
            subtitle="DM Creatives Operating System"
          />
          <div className="flex items-center gap-2">
            <Badge variant="secondary">Milestone 4</Badge>
            <Button asChild variant="outline" size="sm" className="cursor-pointer">
              <Link href="/login">Sign in</Link>
            </Button>
            <Button asChild size="sm" className="cursor-pointer">
              <Link href={configured ? "/signup" : "/setup"}>
                {configured ? "Get started" : "Setup"}
              </Link>
            </Button>
          </div>
        </div>
      </header>

      <main className="mx-auto flex w-full max-w-5xl flex-1 flex-col gap-10 px-6 py-12">
        <section className="space-y-4">
          <Badge variant="outline" className="border-primary/30 text-primary">
            App shell ready
          </Badge>
          <h1 className="max-w-2xl text-4xl font-semibold tracking-tight text-foreground sm:text-5xl">
            Your agency operating system starts here.
          </h1>
          <p className="max-w-xl text-base leading-relaxed text-muted-foreground sm:text-lg">
            Milestone 3 polishes the dashboard shell with your DMC brand,
            active navigation, mobile menu, and reusable empty/loading patterns.
          </p>
          <div className="flex flex-wrap gap-3 pt-2">
            <Button asChild className="cursor-pointer">
              <Link href={configured ? "/dashboard" : "/setup"}>
                {configured ? "Open dashboard" : "Connect Supabase"}
              </Link>
            </Button>
            <Button asChild variant="outline" className="cursor-pointer">
              <Link href="/login">Sign in</Link>
            </Button>
          </div>
        </section>

        <Separator />

        <section className="grid gap-6 md:grid-cols-2">
          <Card className="border-border/80 shadow-sm">
            <CardHeader>
              <CardTitle>Progress checklist</CardTitle>
              <CardDescription>
                What is done and what comes next.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {foundationChecks.map((item) => (
                <div key={item.label} className="flex items-start gap-3">
                  {item.done ? (
                    <CheckCircle2
                      className="mt-0.5 size-4 shrink-0 text-primary"
                      aria-hidden
                    />
                  ) : (
                    <Circle
                      className="mt-0.5 size-4 shrink-0 text-muted-foreground"
                      aria-hidden
                    />
                  )}
                  <span
                    className={
                      item.done
                        ? "text-sm text-foreground"
                        : "text-sm text-muted-foreground"
                    }
                  >
                    {item.label}
                  </span>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card id="tokens" className="scroll-mt-8 border-border/80 shadow-sm">
            <CardHeader>
              <CardTitle>Studio Command tokens</CardTitle>
              <CardDescription>
                Shared colors used by every screen and shadcn component.
              </CardDescription>
            </CardHeader>
            <CardContent className="grid gap-4 sm:grid-cols-2">
              {tokens.map((token) => (
                <TokenSwatch
                  key={token.name}
                  name={token.name}
                  value={token.value}
                  className={token.className}
                />
              ))}
            </CardContent>
          </Card>
        </section>
      </main>

      <footer className="border-t border-border/80 py-6">
        <p className="mx-auto max-w-5xl px-6 text-sm text-muted-foreground">
          DM OS · Milestone 3 App Shell · DM Creatives Studio
        </p>
      </footer>
    </div>
  );
}
