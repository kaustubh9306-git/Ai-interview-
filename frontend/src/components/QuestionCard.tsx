interface QuestionCardProps {
  question: string;
  questionNumber: number;
}

export function QuestionCard({ question, questionNumber }: QuestionCardProps) {
  return (
    <div
      key={questionNumber}
      className="animate-fade-up rounded-2xl border border-border bg-surface p-7 shadow-[0_1px_2px_rgba(18,20,28,0.04),0_16px_40px_-20px_rgba(18,20,28,0.14)] sm:p-9"
    >
      <div className="flex items-center gap-2.5">
        <span aria-hidden="true" className="h-1.5 w-1.5 rounded-full bg-accent" />
        <span className="font-mono text-[11px] uppercase tracking-wider text-accent">
          AI Interviewer
        </span>
        <span className="font-mono text-[11px] text-ink-faint">
          Q{String(questionNumber).padStart(2, "0")}
        </span>
      </div>

      <p className="mt-4 font-display text-[24px] leading-[1.4] tracking-tight text-ink sm:text-[27px]">
        {question}
      </p>
    </div>
  );
}
