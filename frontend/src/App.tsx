import { AppShell } from "./components/AppShell";
import { DEMO_CANDIDATE } from "./config/demoCandidate";
import { useInterview } from "./hooks/useInterview";
import { InterviewPage } from "./pages/InterviewPage";
import { LandingPage } from "./pages/LandingPage";

export default function App() {
  const {
    state,
    messages,
    error,
    questionCount,
    sessionId,
    feedback,
    begin,
    submitAnswer,
    retryLastAction,
    restart,
  } = useInterview();

  return (
    <AppShell>
      {state === "IDLE" ? (
        <LandingPage
          onStart={() => begin(DEMO_CANDIDATE)}
          isStarting={false}
          error={error}
        />
      ) : (
        <InterviewPage
          state={state}
          messages={messages}
          error={error}
          questionCount={questionCount}
          sessionId={sessionId}
          feedback={feedback}
          onSubmitAnswer={submitAnswer}
          onRetry={retryLastAction}
          onRestart={restart}
        />
      )}
    </AppShell>
  );
}
