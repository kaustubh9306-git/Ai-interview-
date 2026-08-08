import { AnswerComposer } from "../components/AnswerComposer";
import { CompletionScreen } from "../components/CompletionScreen";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import { MessageHistory } from "../components/MessageHistory";
import { QuestionCard } from "../components/QuestionCard";
import { SessionRail } from "../components/SessionRail";
import { SiteHeader } from "../components/SiteHeader";
import { DEMO_CANDIDATE } from "../config/demoCandidate";

import type {
  InterviewError,
  InterviewMessage,
  InterviewState,
  InterviewFeedback,
} from "../types/interview";

interface InterviewPageProps {
  state: InterviewState;
  messages: InterviewMessage[];
  error: InterviewError | null;
  questionCount: number;
  sessionId: string | null;
  feedback: InterviewFeedback | null;
  onSubmitAnswer: (text: string) => void;
  onRetry: () => void;
  onRestart: () => void;
}

export function InterviewPage({
  state,
  messages,
  error,
  questionCount,
  sessionId,
  feedback,
  onSubmitAnswer,
  onRetry,
  onRestart,
}: InterviewPageProps) {
  const interviewerMessages = messages.filter(
    (message) => message.role === "interviewer"
  );

  const latestQuestion =
    interviewerMessages[interviewerMessages.length - 1];

  const earlierMessages = messages.slice(0, -1);

  return (
    <div className="min-h-screen bg-background">
      <SiteHeader
        right={
          <div className="flex items-center gap-3">
            <span className="text-sm font-medium">
              Technical Interview
            </span>

            {state === "COMPLETED" && (
              <span className="rounded-full bg-green-100 px-3 py-1 font-mono text-xs font-medium text-green-700">
                COMPLETE
              </span>
            )}

            {state === "ERROR" && (
              <span className="rounded-full bg-red-100 px-3 py-1 font-mono text-xs font-medium text-red-700">
                ERROR
              </span>
            )}

            {(state === "QUESTION" || state === "SUBMITTING") && (
              <span className="rounded-full bg-blue-100 px-3 py-1 font-mono text-xs font-medium text-blue-700">
                LIVE
              </span>
            )}
          </div>
        }
      />

      <main className="mx-auto flex w-full max-w-5xl flex-1 flex-col gap-6 px-6 py-8 sm:px-10 lg:flex-row lg:items-start">
        <div className="min-w-0 flex-1">
          {state === "STARTING" && (
            <LoadingState label="Starting your interview…" />
          )}

          {state === "ERROR" && error && (
            <ErrorState
              error={error}
              onRetry={onRetry}
              onRestart={onRestart}
            />
          )}

          {(state === "QUESTION" || state === "SUBMITTING") &&
            latestQuestion && (
              <>
                <QuestionCard
                  question={latestQuestion.content}
                  questionNumber={questionCount}
                />

                <AnswerComposer
                  onSubmit={onSubmitAnswer}
                  isSubmitting={state === "SUBMITTING"}
                />

                <MessageHistory messages={earlierMessages} />
              </>
            )}

          {state === "COMPLETED" && (
            <CompletionScreen
              finalMessage={
                latestQuestion?.content || "Interview completed."
              }
              questionCount={questionCount}
              feedback={feedback}
              onRestart={onRestart}
            />
          )}
        </div>

        {sessionId && state !== "STARTING" && (
          <SessionRail
            candidate={DEMO_CANDIDATE}
            sessionId={sessionId}
            questionCount={questionCount}
            state={state}
          />
        )}
      </main>
    </div>
  );
}