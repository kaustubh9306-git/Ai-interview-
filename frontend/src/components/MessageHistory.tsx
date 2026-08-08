import { useState } from "react";
import { ChevronDown } from "lucide-react";
import type { InterviewMessage } from "../types/interview";

export function MessageHistory({ messages }: { messages: InterviewMessage[] }) {
  const [open, setOpen] = useState(false);

  if (messages.length === 0) return null;

  return (
    <div className="mt-6 border-t border-border-soft pt-4">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="flex items-center gap-1.5 font-mono text-xs uppercase tracking-wider text-ink-faint transition-colors hover:text-ink-muted"
        aria-expanded={open}
      >
        <ChevronDown
          size={13}
          className={`transition-transform ${open ? "rotate-180" : ""}`}
          aria-hidden="true"
        />
        Earlier in this interview
      </button>

      {open && (
        <ol className="thin-scroll mt-3 max-h-64 space-y-3 overflow-y-auto pr-1">
          {messages.map((m) => (
            <li key={m.id} className="text-sm leading-snug">
              <span
                className={`font-mono text-[10px] uppercase tracking-wider ${
                  m.role === "interviewer" ? "text-accent" : "text-ink-faint"
                }`}
              >
                {m.role === "interviewer" ? "Interviewer" : "You"}
              </span>
              <p className="mt-0.5 text-ink-muted">{m.content}</p>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}
