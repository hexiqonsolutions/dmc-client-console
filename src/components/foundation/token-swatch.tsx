import { cn } from "@/lib/utils";

type TokenSwatchProps = {
  name: string;
  value: string;
  className?: string;
};

export function TokenSwatch({ name, value, className }: TokenSwatchProps) {
  return (
    <div className="flex items-center gap-3">
      <div
        className={cn(
          "size-10 shrink-0 rounded-md border border-border shadow-sm",
          className,
        )}
        aria-hidden
      />
      <div className="min-w-0">
        <p className="truncate text-sm font-medium text-foreground">{name}</p>
        <p className="truncate font-mono text-xs text-muted-foreground">
          {value}
        </p>
      </div>
    </div>
  );
}
