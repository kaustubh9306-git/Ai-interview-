export function LoadingState({ label }: { label: string }) {
  return (
    <div
      role="status"
      className="flex min-h-[240px] flex-col items-center justify-center gap-3 rounded-2xl border border-border bg-surface p-9"
    >
      <span
        aria-hidden="true"
        className="h-2 w-2 rounded-full bg-accent animate-pulse-soft"
      />
      <p className="font-mono text-xs uppercase tracking-wider text-ink-faint">
        {label}
      </p>
    </div>
  );
}
