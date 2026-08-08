import type { ReactNode } from "react";

export function SiteHeader({ right }: { right?: ReactNode }) {
  return (
    <header className="flex items-center justify-between border-b border-border px-6 py-5 sm:px-10">
      <div className="flex items-center gap-2.5">
        <span
          aria-hidden="true"
          className="flex h-7 w-7 items-center justify-center rounded-md bg-ink font-mono text-[13px] font-medium text-white"
        >
          AI
        </span>
        <span className="font-display text-[19px] leading-none tracking-tight">
          AI Interviewer
        </span>
      </div>
      {right}
    </header>
  );
}
