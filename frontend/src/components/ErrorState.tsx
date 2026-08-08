import { AlertTriangle } from "lucide-react";
import type { InterviewError } from "../types/interview";

interface ErrorStateProps {
  error: InterviewError;
  onRetry: () => void;
  onRestart: () => void;
}

export function ErrorState({ error, onRetry, onRestart }: ErrorStateProps) {
  return (
    <div
      role="alert"
      className="animate-fade-up rounded-2xl border border-danger-soft bg-danger-soft p-7 sm:p-9"
    >
      <div className="flex items-start gap-3">
        <AlertTriangle
          size={20}
          className="mt-0.5 shrink-0 text-danger"
          aria-hidden="true"
        />
        <div>
          <p className="font-medium text-ink">Something went wrong</p>
          <p className="mt-1 text-sm leading-relaxed text-ink-muted">
            {error.message}
          </p>
        </div>
      </div>

      <div className="mt-5 flex gap-3">
        {error.retryable && (
          <button
            type="button"
            onClick={onRetry}
            className="rounded-lg bg-ink px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-accent-dark"
          >
            Retry
          </button>
        )}
        <button
          type="button"
          onClick={onRestart}
          className="rounded-lg border border-border-strong bg-surface px-4 py-2 text-sm font-medium text-ink transition-colors hover:bg-border-soft"
        >
          Start Over
        </button>
      </div>
    </div>
  );
}
