import type { Candidate } from "../types/interview";

interface CandidateCardProps {
  candidate: Candidate;
  onStart: () => void;
  disabled?: boolean;
  isStarting?: boolean;
}

export function CandidateCard({
  candidate,
  onStart,
  disabled,
  isStarting,
}: CandidateCardProps) {
  const { member } = candidate;

  return (
    <div className="w-full max-w-sm rounded-2xl border border-border bg-surface shadow-[0_1px_2px_rgba(18,20,28,0.04),0_12px_32px_-16px_rgba(18,20,28,0.12)]">
      <div className="flex items-center justify-between border-b border-border-soft px-6 py-4">
        <span className="font-mono text-[11px] uppercase tracking-wider text-ink-faint">
          Session candidate
        </span>
        <span className="font-mono text-[11px] text-ink-faint">
          {member.id}
        </span>
      </div>

      <div className="px-6 py-6">
        <p className="font-display text-2xl leading-tight">{member.name}</p>
        <p className="mt-1 text-sm text-ink-muted">{member.jobRole}</p>

        <dl className="mt-5 space-y-2.5 border-t border-border-soft pt-5 text-sm">
          <Row label="Experience" value={`${member.yearsExperience} years`} />
          <Row label="Education" value={member.education} />
          <Row label="Status" value={member.status} />
        </dl>

        <button
          type="button"
          onClick={onStart}
          disabled={disabled}
          className="mt-6 flex w-full items-center justify-center rounded-lg bg-ink px-4 py-3 text-sm font-medium text-white transition-colors hover:bg-accent-dark disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isStarting ? "Starting interview…" : "Start Interview"}
        </button>
        <p className="mt-3 text-center text-xs text-ink-faint">
          Your interview will adapt based on your responses.
        </p>
      </div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between">
      <dt className="text-ink-muted">{label}</dt>
      <dd className="font-medium text-ink">{value}</dd>
    </div>
  );
}
