import Image from "next/image";
import Link from "next/link";

import { cn } from "@/lib/utils";

type BrandLogoProps = {
  href?: string;
  className?: string;
  /** Compact circular mark (favicon) vs full wordmark */
  variant?: "mark" | "wordmark";
  showWordmark?: boolean;
  subtitle?: string | null;
  /** Prefer light treatment on dark surfaces (ink sidebar) */
  onDark?: boolean;
};

export function BrandLogo({
  href = "/",
  className,
  variant = "mark",
  showWordmark = true,
  subtitle,
  onDark = false,
}: BrandLogoProps) {
  const content = (
    <span className={cn("flex min-w-0 items-center gap-3", className)}>
      {variant === "wordmark" ? (
        <span
          className={cn(
            "relative block h-8 w-[7.5rem] overflow-hidden rounded-md",
            onDark ? "bg-white/95" : "bg-black",
          )}
        >
          <Image
            src="/dm-logo.png"
            alt="DM Creatives"
            fill
            className="object-contain object-left p-1"
            sizes="120px"
            priority
          />
        </span>
      ) : (
        <span className="relative size-9 shrink-0 overflow-hidden rounded-full bg-white ring-1 ring-border/60">
          <Image
            src="/favicon.png"
            alt="DM Creatives"
            fill
            className="object-cover"
            sizes="36px"
            priority
          />
        </span>
      )}

      {showWordmark ? (
        <span className="min-w-0">
          <span
            className={cn(
              "block truncate font-heading text-sm font-semibold tracking-tight",
              onDark ? "text-sidebar-foreground" : "text-foreground",
            )}
          >
            DM OS
          </span>
          {subtitle ? (
            <span
              className={cn(
                "block truncate text-xs",
                onDark
                  ? "text-sidebar-foreground/70"
                  : "text-muted-foreground",
              )}
            >
              {subtitle}
            </span>
          ) : null}
        </span>
      ) : null}
    </span>
  );

  if (!href) {
    return content;
  }

  return (
    <Link href={href} className="outline-none transition-opacity hover:opacity-90 focus-visible:ring-2 focus-visible:ring-ring">
      {content}
    </Link>
  );
}
