import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

type PageLoadingProps = {
  className?: string;
  cards?: number;
};

export function PageLoading({ className, cards = 2 }: PageLoadingProps) {
  return (
    <div className={cn("mx-auto flex w-full max-w-5xl flex-col gap-6", className)}>
      <div className="space-y-3">
        <Skeleton className="h-5 w-24" />
        <Skeleton className="h-9 w-64 max-w-full" />
        <Skeleton className="h-4 w-96 max-w-full" />
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {Array.from({ length: cards }).map((_, index) => (
          <Skeleton key={index} className="h-40 rounded-xl" />
        ))}
      </div>
    </div>
  );
}
