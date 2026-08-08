interface StatusBadgeProps {
  label: string;
  tone?: "live" | "neutral" | "success" | "danger";
}

const toneClasses: Record<Required<StatusBadgeProps>["tone"], string> = {
  live: "bg-accent-soft text-accent-dark",
  neutral: "bg-border-soft text-ink-muted",
  success: "bg-success-soft text-success",
  danger: "bg-danger-soft text-danger",
};

export function StatusBadge({ label, tone = "neutral" }: StatusBadgeProps) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 font-mono text-[11px] font-medium uppercase tracking-wider ${toneClasses[tone]}`}
    >
      {tone === "live" && (
        <span
          aria-hidden="true"
          className="h-1.5 w-1.5 rounded-full bg-accent animate-pulse-soft"
        />
      )}
      {label}
    </span>
  );
}
