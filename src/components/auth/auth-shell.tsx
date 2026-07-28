import { BrandLogo } from "@/components/brand/brand-logo";

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
        <div className="mx-auto flex w-full max-w-lg items-center px-6 py-4">
          <BrandLogo href="/" variant="wordmark" showWordmark={false} />
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
