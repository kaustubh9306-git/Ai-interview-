import { useState, type FormEvent, type KeyboardEvent } from "react";
import { CornerDownLeft } from "lucide-react";

interface AnswerComposerProps {
  onSubmit: (text: string) => void;
  isSubmitting: boolean;
}

export function AnswerComposer({ onSubmit, isSubmitting }: AnswerComposerProps) {
  const [value, setValue] = useState("");
  const trimmedLength = value.trim().length;
  const canSubmit = trimmedLength > 0 && !isSubmitting;

  function submit() {
    if (!canSubmit) return;
    onSubmit(value);
    setValue("");
  }

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    submit();
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && (event.metaKey || event.ctrlKey)) {
      event.preventDefault();
      submit();
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mt-5">
      <label htmlFor="candidate-answer" className="sr-only">
        Your answer
      </label>
      <textarea
        id="candidate-answer"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={isSubmitting}
        placeholder="Type your answer here…"
        rows={7}
        className="w-full resize-y rounded-xl border border-border bg-surface px-4 py-3.5 text-[15px] leading-relaxed text-ink placeholder:text-ink-faint focus-visible:border-accent disabled:bg-border-soft disabled:text-ink-muted"
      />

      <div className="mt-3 flex items-center justify-between">
        <span className="font-mono text-xs text-ink-faint">
          {trimmedLength > 0 ? `${trimmedLength} characters` : "⌘/Ctrl + Enter to submit"}
        </span>

        <button
          type="submit"
          disabled={!canSubmit}
          className="flex items-center gap-2 rounded-lg bg-ink px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-accent-dark disabled:cursor-not-allowed disabled:opacity-40"
        >
          {isSubmitting ? (
            "AI is evaluating your answer…"
          ) : (
            <>
              Submit Answer
              <CornerDownLeft size={14} aria-hidden="true" />
            </>
          )}
        </button>
      </div>
    </form>
  );
}
