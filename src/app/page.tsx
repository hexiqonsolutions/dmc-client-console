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
import { TokenSwatch } from "@/components/foundation/token-swatch";
import { CheckCircle2, Circle } from "lucide-react";

const foundationChecks = [
  { label: "Next.js App Router + TypeScript", done: true },
  { label: "Tailwind CSS v4", done: true },
  { label: "shadcn/ui base components", done: true },
  { label: "Studio Command design tokens", done: true },
  { label: "Project documentation", done: true },
  { label: "Auth & Supabase (Milestone 2)", done: false },
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
  return (
    <div className="flex flex-1 flex-col">
      <header className="border-b border-border/80 bg-card/80 backdrop-blur-sm">
        <div className="mx-auto flex w-full max-w-5xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex size-9 items-center justify-center rounded-md bg-sidebar text-sm font-semibold tracking-tight text-sidebar-primary-foreground">
              <span className="text-sidebar-primary">DM</span>
            </div>
            <div>
              <p className="font-heading text-lg font-semibold tracking-tight text-foreground">
                DM OS
              </p>
              <p className="text-xs text-muted-foreground">
                DM Creatives Operating System
              </p>
            </div>
          </div>
          <Badge variant="secondary">Milestone 1</Badge>
        </div>
      </header>

      <main className="mx-auto flex w-full max-w-5xl flex-1 flex-col gap-10 px-6 py-12">
        <section className="space-y-4">
          <Badge variant="outline" className="border-primary/30 text-primary">
            Foundation ready
          </Badge>
          <h1 className="max-w-2xl text-4xl font-semibold tracking-tight text-foreground sm:text-5xl">
            Your agency operating system starts here.
          </h1>
          <p className="max-w-xl text-base leading-relaxed text-muted-foreground sm:text-lg">
            Milestone 1 locks the production stack and Studio Command design
            system. Auth, database, and modules come next — one milestone at a
            time.
          </p>
          <div className="flex flex-wrap gap-3 pt-2">
            <Button className="cursor-pointer" type="button">
              Foundation complete
            </Button>
            <Button variant="outline" className="cursor-pointer" asChild>
              <a href="#tokens">View design tokens</a>
            </Button>
          </div>
        </section>

        <Separator />

        <section className="grid gap-6 md:grid-cols-2">
          <Card className="border-border/80 shadow-sm">
            <CardHeader>
              <CardTitle>Foundation checklist</CardTitle>
              <CardDescription>
                What Milestone 1 delivers and what comes next.
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

        <section className="rounded-xl border border-border/80 bg-card/90 p-6 shadow-sm">
          <h2 className="text-xl font-semibold tracking-tight">
            Component smoke test
          </h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Verify buttons, badges, and focus styles render with the design
            system.
          </p>
          <div className="mt-5 flex flex-wrap items-center gap-3">
            <Button className="cursor-pointer">Primary</Button>
            <Button variant="secondary" className="cursor-pointer">
              Secondary
            </Button>
            <Button variant="outline" className="cursor-pointer">
              Outline
            </Button>
            <Button
              className="cursor-pointer bg-cta text-cta-foreground hover:bg-cta/90"
            >
              CTA
            </Button>
            <Badge>Default</Badge>
            <Badge variant="secondary">Secondary</Badge>
            <Badge variant="outline">Outline</Badge>
          </div>
        </section>
      </main>

      <footer className="border-t border-border/80 py-6">
        <p className="mx-auto max-w-5xl px-6 text-sm text-muted-foreground">
          DM OS · Milestone 1 Foundation · DM Creatives Studio
        </p>
      </footer>
    </div>
  );
}
