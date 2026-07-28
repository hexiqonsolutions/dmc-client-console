import Link from "next/link";

export function AuthShell({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-full flex-1 flex-col">
      <header className="border-b border-border/80 bg-card/80 backdrop-blur-sm">
        <div className="mx-auto flex w-full max-w-lg items-center justify-between px-6 py-4">
          <Link href="/" className="flex items-center gap-3">
            <div className="flex size-9 items-center justify-center rounded-md bg-sidebar text-sm font-semibold tracking-tight">
              <span className="text-sidebar-primary">DM</span>
            </div>
            <span className="font-heading text-lg font-semibold tracking-tight text-foreground">
              DM OS
            </span>
          </Link>
        </div>
      </header>

      <main className="mx-auto flex w-full max-w-lg flex-1 flex-col justify-center px-6 py-12">
        <div className="mb-8 space-y-2">
          <h1 className="text-3xl font-semibold tracking-tight text-foreground">
            {title}
          </h1>
          <p className="text-sm leading-relaxed text-muted-foreground">
            {description}
          </p>
        </div>
        <div className="rounded-xl border border-border/80 bg-card p-6 shadow-sm">
          {children}
        </div>
      </main>
    </div>
  );
}
