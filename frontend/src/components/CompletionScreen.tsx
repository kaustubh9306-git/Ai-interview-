import { Check, Trophy, Target, AlertTriangle, ArrowRight } from "lucide-react";

import type { InterviewFeedback } from "../types/interview";

interface CompletionScreenProps {
  finalMessage: string;
  questionCount: number;
  feedback: InterviewFeedback | null;
  onRestart: () => void;
}

export function CompletionScreen({
  finalMessage,
  questionCount,
  feedback,
  onRestart,
}: CompletionScreenProps) {
  const score = feedback?.average_score;
  const totalQuestions =
    feedback?.total_questions ?? questionCount;

  return (
    <div className="w-full">
      {/* Header */}
      <div className="text-center">
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-green-100 text-green-700">
          <Check size={28} strokeWidth={2.5} />
        </div>

        <h2 className="mt-5 font-display text-3xl tracking-tight">
          Interview Complete
        </h2>

        <p className="mx-auto mt-3 max-w-md text-[15px] leading-relaxed text-ink-muted">
          {finalMessage}
        </p>
      </div>

      {/* Stats */}
      <div className="mt-8 grid gap-4 sm:grid-cols-2">
        <div className="rounded-xl border border-border bg-white p-6 text-center shadow-sm">
          <Trophy className="mx-auto h-6 w-6 text-accent" />

          <p className="mt-3 text-xs font-medium uppercase tracking-wider text-ink-faint">
            Technical Score
          </p>

          <p className="mt-2 font-display text-4xl font-semibold">
            {score !== undefined ? `${score}/10` : "—"}
          </p>
        </div>

        <div className="rounded-xl border border-border bg-white p-6 text-center shadow-sm">
          <Target className="mx-auto h-6 w-6 text-accent" />

          <p className="mt-3 text-xs font-medium uppercase tracking-wider text-ink-faint">
            Questions Evaluated
          </p>

          <p className="mt-2 font-display text-4xl font-semibold">
            {totalQuestions}
          </p>
        </div>
      </div>

      {/* Summary */}
      {feedback && (
        <>
          <div className="mt-6 rounded-xl border border-border bg-white p-6 shadow-sm">
            <h3 className="text-sm font-semibold">
              Interview Summary
            </h3>

            <p className="mt-3 text-sm leading-relaxed text-ink-muted">
              {feedback.summary}
            </p>
          </div>

          {/* Strengths */}
          <div className="mt-6 rounded-xl border border-border bg-white p-6 shadow-sm">
            <h3 className="text-sm font-semibold">
              Strengths
            </h3>

            {feedback.strengths.length > 0 ? (
              <ul className="mt-4 space-y-3">
                {feedback.strengths.map((strength, index) => (
                  <li
                    key={`${strength}-${index}`}
                    className="flex gap-3 text-sm text-ink-muted"
                  >
                    <Check
                      size={17}
                      className="mt-0.5 shrink-0 text-green-600"
                    />
                    <span>{strength}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-3 text-sm text-ink-faint">
                No specific strengths were recorded.
              </p>
            )}
          </div>

          {/* Gaps */}
          <div className="mt-6 rounded-xl border border-border bg-white p-6 shadow-sm">
            <h3 className="text-sm font-semibold">
              Areas to Improve
            </h3>

            {feedback.gaps.length > 0 ? (
              <ul className="mt-4 space-y-3">
                {feedback.gaps.map((gap, index) => (
                  <li
                    key={`${gap}-${index}`}
                    className="flex gap-3 text-sm text-ink-muted"
                  >
                    <AlertTriangle
                      size={17}
                      className="mt-0.5 shrink-0 text-amber-600"
                    />
                    <span>{gap}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-3 text-sm text-ink-faint">
                No specific gaps were recorded.
              </p>
            )}
          </div>

          {/* Next steps */}
          <div className="mt-6 rounded-xl border border-border bg-white p-6 shadow-sm">
            <h3 className="text-sm font-semibold">
              Recommended Next Steps
            </h3>

            {feedback.next.length > 0 ? (
              <ul className="mt-4 space-y-3">
                {feedback.next.map((item, index) => (
                  <li
                    key={`${item}-${index}`}
                    className="flex gap-3 text-sm text-ink-muted"
                  >
                    <ArrowRight
                      size={17}
                      className="mt-0.5 shrink-0 text-accent"
                    />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-3 text-sm text-ink-faint">
                No additional recommendations were recorded.
              </p>
            )}
          </div>
        </>
      )}

      {/* Question count */}
      <p className="mt-6 text-center font-mono text-xs uppercase tracking-wider text-ink-faint">
        {questionCount} question
        {questionCount === 1 ? "" : "s"} asked this session
      </p>

      {/* Restart */}
      <div className="mt-8 flex justify-center">
        <button
          type="button"
          onClick={onRestart}
          className="rounded-lg bg-ink px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-accent-dark"
        >
          Start New Interview
        </button>
      </div>
    </div>
  );
}