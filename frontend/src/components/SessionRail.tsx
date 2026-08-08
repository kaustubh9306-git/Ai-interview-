import type { Candidate, InterviewState } from "../types/interview";
import { StatusBadge } from "./StatusBadge";

interface SessionRailProps {
  candidate: Candidate;
  sessionId: string;
  questionCount: number;
  state: InterviewState;
}

export function SessionRail({
  candidate,
  sessionId,
  questionCount,
  state,
}: SessionRailProps) {
  const { member } = candidate;
  const shortSessionId = sessionId.split("-")[0];

  return (
    <aside className="w-full shrink-0 lg:w-64">
      <div className="rounded-2xl border border-border bg-surface p-5">
        <span className="font-mono text-[11px] uppercase tracking-wider text-ink-faint">
          Session
        </span>
        <p className="mt-1.5 font-mono text-sm text-ink">{shortSessionId}</p>

        <div className="mt-4">
          <SessionStatus state={state} />
        </div>

        <div className="mt-5 border-t border-border-soft pt-4">
          <p className="text-sm font-medium text-ink">{member.name}</p>
          <p className="mt-0.5 text-xs text-ink-muted">{member.jobRole}</p>
        </div>

        <div className="mt-5 border-t border-border-soft pt-4">
          <span className="font-mono text-[11px] uppercase tracking-wider text-ink-faint">
            Interview log
          </span>
          <ul className="mt-3 space-y-1.5" aria-label="Questions asked so far">
            {Array.from({ length: questionCount }, (_, i) => (
              <li
                key={i}
                className="flex items-center gap-2.5 font-mono text-xs text-ink-muted"
              >
                <span
                  aria-hidden="true"
                  className="h-px w-3 bg-border-strong"
                />
                Q{String(i + 1).padStart(2, "0")} answered
              </li>
            ))}
            {questionCount === 0 && (
              <li className="font-mono text-xs text-ink-faint">
                Awaiting first question
              </li>
            )}
          </ul>
        </div>
      </div>
    </aside>
  );
}

function SessionStatus({ state }: { state: InterviewState }) {
  switch (state) {
    case "COMPLETED":
      return <StatusBadge label="Complete" tone="success" />;
    case "ERROR":
      return <StatusBadge label="Error" tone="danger" />;
    case "QUESTION":
    case "SUBMITTING":
    case "STARTING":
      return <StatusBadge label="Live" tone="live" />;
    default:
      return <StatusBadge label="Idle" tone="neutral" />;
  }
}
