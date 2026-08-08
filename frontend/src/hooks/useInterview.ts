import {
  useCallback,
  useRef,
  useState,
} from "react";

import {
  sendAnswer,
  startInterview,
} from "../services/interviewApi";

import {
  InterviewApiError,
} from "../services/interviewApiError";

import type {
  Candidate,
  InterviewError,
  InterviewFeedback,
  InterviewMessage,
  InterviewState,
} from "../types/interview";

interface UseInterviewResult {
  state: InterviewState;
  messages: InterviewMessage[];
  error: InterviewError | null;
  questionCount: number;
  sessionId: string | null;
  feedback: InterviewFeedback | null;

  begin: (
    candidate: Candidate
  ) => Promise<void>;

  submitAnswer: (
    text: string
  ) => Promise<void>;

  retryLastAction: () => Promise<void>;

  restart: () => void;
}

function makeMessage(
  role: InterviewMessage["role"],
  content: string
): InterviewMessage {
  return {
    id: crypto.randomUUID(),
    role,
    content,
    timestamp: new Date().toISOString(),
  };
}

function generateSessionId(): string {
  return crypto.randomUUID();
}

export function useInterview(): UseInterviewResult {
  const [state, setState] =
    useState<InterviewState>("IDLE");

  const [messages, setMessages] =
    useState<InterviewMessage[]>([]);

  const [error, setError] =
    useState<InterviewError | null>(null);

  const [sessionId, setSessionId] =
    useState<string | null>(null);

  const [feedback, setFeedback] =
    useState<InterviewFeedback | null>(null);

  const lastActionRef = useRef<
    | {
        type: "start";
        candidate: Candidate;
      }
    | {
        type: "answer";
        text: string;
      }
    | null
  >(null);

  const questionCount =
    messages.filter(
      (message) =>
        message.role === "interviewer"
    ).length;

  const handleFailure = useCallback(
    (err: unknown) => {
      if (
        err instanceof InterviewApiError
      ) {
        setError({
          message: err.message,
          retryable: err.retryable,
          statusCode: err.statusCode,
        });
      } else {
        console.error(
          "Unexpected interview error:",
          err
        );

        setError({
          message:
            "Something unexpected went wrong. Please try again.",
          retryable: true,
        });
      }

      setState("ERROR");
    },
    []
  );

  const begin = useCallback(
    async (candidate: Candidate) => {
      const newSessionId =
        generateSessionId();

      setSessionId(newSessionId);
      setMessages([]);
      setFeedback(null);
      setError(null);
      setState("STARTING");

      lastActionRef.current = {
        type: "start",
        candidate,
      };

      try {
        const response =
          await startInterview(
            newSessionId,
            candidate
          );

        setMessages([
          makeMessage(
            "interviewer",
            response.reply
          ),
        ]);

        if (response.done) {
          setFeedback(
            response.feedback ?? null
          );

          setState("COMPLETED");
        } else {
          setState("QUESTION");
        }
      } catch (err) {
        handleFailure(err);
      }
    },
    [handleFailure]
  );

  const submitAnswer = useCallback(
    async (text: string) => {
      const trimmed =
        text.trim();

      if (
        !trimmed ||
        !sessionId
      ) {
        return;
      }

      setMessages(
        (previous) => [
          ...previous,
          makeMessage(
            "candidate",
            trimmed
          ),
        ]
      );

      setError(null);
      setState("SUBMITTING");

      lastActionRef.current = {
        type: "answer",
        text: trimmed,
      };

      try {
        const response =
          await sendAnswer(
            sessionId,
            trimmed
          );

        setMessages(
          (previous) => [
            ...previous,
            makeMessage(
              "interviewer",
              response.reply
            ),
          ]
        );

        if (response.done) {
          setFeedback(
            response.feedback ?? null
          );

          setState("COMPLETED");
        } else {
          setState("QUESTION");
        }
      } catch (err) {
        handleFailure(err);
      }
    },
    [
      sessionId,
      handleFailure,
    ]
  );

  const retryLastAction =
    useCallback(
      async () => {
        const action =
          lastActionRef.current;

        if (!action) {
          return;
        }

        if (
          action.type === "start"
        ) {
          await begin(
            action.candidate
          );

          return;
        }

        if (!sessionId) {
          return;
        }

        setError(null);
        setState("SUBMITTING");

        try {
          const response =
            await sendAnswer(
              sessionId,
              action.text
            );

          setMessages(
            (previous) => [
              ...previous,
              makeMessage(
                "interviewer",
                response.reply
              ),
            ]
          );

          if (response.done) {
            setFeedback(
              response.feedback ?? null
            );

            setState("COMPLETED");
          } else {
            setState("QUESTION");
          }
        } catch (err) {
          handleFailure(err);
        }
      },
      [
        begin,
        sessionId,
        handleFailure,
      ]
    );

  const restart =
    useCallback(() => {
      setState("IDLE");
      setMessages([]);
      setError(null);
      setSessionId(null);
      setFeedback(null);
      lastActionRef.current = null;
    }, []);

  return {
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
  };
}