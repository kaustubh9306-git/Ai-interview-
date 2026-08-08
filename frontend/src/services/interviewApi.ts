import type {
  Candidate,
  InterviewResponse,
  SendAnswerRequest,
  StartInterviewRequest,
} from "../types/interview";

import { InterviewApiError } from "./interviewApiError";

const API_BASE_URL =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ??
  "http://127.0.0.1:8000";

const INTERVIEW_ENDPOINT =
  `${API_BASE_URL}/api/interview`;

function assertIsInterviewResponse(
  value: unknown
): InterviewResponse {
  if (
    typeof value === "object" &&
    value !== null &&
    "reply" in value &&
    typeof (value as { reply: unknown }).reply === "string" &&
    "done" in value &&
    typeof (value as { done: unknown }).done === "boolean"
  ) {
    return value as InterviewResponse;
  }

  throw new InterviewApiError(
    "The interview server returned an unexpected response format.",
    {
      retryable: true,
    }
  );
}

async function postInterview(
  body: StartInterviewRequest | SendAnswerRequest
): Promise<InterviewResponse> {
  let response: Response;

  try {
    response = await fetch(INTERVIEW_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
  } catch (error) {
    console.error(
      "Network error contacting interview API:",
      error
    );

    throw new InterviewApiError(
      "Cannot connect to the interview server. Make sure the FastAPI backend is running.",
      {
        retryable: true,
      }
    );
  }

  if (!response.ok) {
    const statusCode = response.status;

    let detail = "";

    try {
      const errorBody = await response.json();

      detail =
        typeof errorBody?.detail === "string"
          ? errorBody.detail
          : JSON.stringify(
              errorBody?.detail ?? ""
            );
    } catch {
      // Ignore invalid JSON error responses.
    }

    console.error(
      `Interview API error ${statusCode}:`,
      detail
    );

    throw new InterviewApiError(
      messageForStatus(statusCode),
      {
        retryable:
          statusCode >= 500 ||
          statusCode === 0,
        statusCode,
      }
    );
  }

  let parsed: unknown;

  try {
    parsed = await response.json();
  } catch {
    throw new InterviewApiError(
      "The interview server returned a malformed response.",
      {
        retryable: true,
      }
    );
  }

  return assertIsInterviewResponse(parsed);
}

function messageForStatus(
  statusCode: number
): string {
  switch (statusCode) {
    case 400:
    case 422:
      return "Unable to process the interview request. Please check the candidate information and try again.";

    case 401:
    case 403:
      return "You are not authorized to access the interview server.";

    case 404:
      return "The interview endpoint could not be found on the backend.";

    case 500:
    case 502:
    case 503:
      return "The interview server encountered an error. Please try again in a moment.";

    default:
      return "Something went wrong while talking to the interview server.";
  }
}

/**
 * Starts a new interview.
 */
export function startInterview(
  sessionId: string,
  candidate: Candidate
): Promise<InterviewResponse> {
  return postInterview({
    sessionId,
    candidate,
  });
}

/**
 * Sends the candidate's answer.
 */
export function sendAnswer(
  sessionId: string,
  message: string
): Promise<InterviewResponse> {
  return postInterview({
    sessionId,
    message,
  });
}