/**
 * Domain types for the AI Interviewer frontend.
 */

/**
 * Candidate object sent to the backend when starting an interview.
 */
export interface Candidate {
  member: {
    id: string;
    name: string;
    jobRole: string;
    yearsExperience: number;
    education: string;
    status: string;
  };
}

/**
 * Request body when starting an interview.
 */
export interface StartInterviewRequest {
  sessionId: string;
  candidate: Candidate;
}

/**
 * Request body when submitting an answer.
 */
export interface SendAnswerRequest {
  sessionId: string;
  message: string;
}

export type InterviewRequest =
  | StartInterviewRequest
  | SendAnswerRequest;

/**
 * Feedback returned by the backend after interview completion.
 */
export interface InterviewFeedback {
  summary: string;
  strengths: string[];
  gaps: string[];
  next: string[];

  /**
   * Average technical score calculated by the backend.
   */
  average_score?: number;

  /**
   * Number of evaluated questions.
   */
  total_questions?: number;
}

/**
 * Response returned by POST /api/interview.
 */
export interface InterviewResponse {
  reply: string;
  done: boolean;
  feedback?: InterviewFeedback;
}

/**
 * Frontend-only transcript message.
 */
export interface InterviewMessage {
  id: string;
  role: "interviewer" | "candidate";
  content: string;
  timestamp: string;
}

/**
 * Interview state machine.
 */
export type InterviewState =
  | "IDLE"
  | "STARTING"
  | "QUESTION"
  | "SUBMITTING"
  | "COMPLETED"
  | "ERROR";

/**
 * Error information shown in the UI.
 */
export interface InterviewError {
  message: string;
  retryable: boolean;
  statusCode?: number;
}