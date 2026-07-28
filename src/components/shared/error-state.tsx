import { AlertCircle } from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

type ErrorStateProps = {
  title?: string;
  description?: string;
  retryHref?: string;
  className?: string;
};

export function ErrorState({
  title = "Something went wrong",
  description = "We could not load this page. Try again in a moment.",
  retryHref,
  className,
}: ErrorStateProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center rounded-xl border border-destructive/20 bg-card px-6 py-14 text-center",
        className,
      )}
      role="alert"
    >
      <div className="mb-4 flex size-12 items-center justify-center rounded-full bg-destructive/10 text-destructive">
        <AlertCircle className="size-5" aria-hidden />
      </div>
      <h2 className="text-base font-semibold tracking-tight text-foreground">
        {title}
      </h2>
      <p className="mt-1 max-w-md text-sm text-muted-foreground">{description}</p>
      {retryHref ? (
        <Button asChild variant="outline" className="mt-5 cursor-pointer">
          <Link href={retryHref}>Try again</Link>
        </Button>
      ) : null}
    </div>
  );
}
