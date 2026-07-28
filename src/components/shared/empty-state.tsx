import { type LucideIcon } from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

type EmptyStateProps = {
  icon?: LucideIcon;
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
  actionHref?: string;
  className?: string;
  children?: React.ReactNode;
};

export function EmptyState({
  icon: Icon,
  title,
  description,
  actionLabel,
  onAction,
  actionHref,
  className,
  children,
}: EmptyStateProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center rounded-xl border border-dashed border-border bg-muted/30 px-6 py-14 text-center",
        className,
      )}
      role="status"
    >
      {Icon ? (
        <div className="mb-4 flex size-12 items-center justify-center rounded-full bg-accent text-accent-foreground">
          <Icon className="size-5" aria-hidden />
        </div>
      ) : null}
      <h2 className="text-base font-semibold tracking-tight text-foreground">
        {title}
      </h2>
      <p className="mt-1 max-w-md text-sm text-muted-foreground">{description}</p>
      {children}
      {actionLabel && (onAction || actionHref) ? (
        <div className="mt-5">
          {actionHref ? (
            <Button asChild className="cursor-pointer">
              <Link href={actionHref}>{actionLabel}</Link>
            </Button>
          ) : (
            <Button type="button" className="cursor-pointer" onClick={onAction}>
              {actionLabel}
            </Button>
          )}
        </div>
      ) : null}
    </div>
  );
}
