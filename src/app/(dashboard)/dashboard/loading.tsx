export default function DashboardLoading() {
  return (
    <div className="mx-auto flex w-full max-w-4xl flex-col gap-4">
      <div className="h-8 w-48 animate-pulse rounded-md bg-muted" />
      <div className="h-4 w-96 max-w-full animate-pulse rounded-md bg-muted" />
      <div className="mt-4 grid gap-4 md:grid-cols-2">
        <div className="h-40 animate-pulse rounded-xl bg-muted" />
        <div className="h-40 animate-pulse rounded-xl bg-muted" />
      </div>
    </div>
  );
}
