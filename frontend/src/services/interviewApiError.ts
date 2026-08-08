export class InterviewApiError extends Error {
  readonly retryable: boolean;
  readonly statusCode?: number;

  constructor(
    message: string,
    options: { retryable: boolean; statusCode?: number },
  ) {
    super(message);
    this.name = "InterviewApiError";
    this.retryable = options.retryable;
    this.statusCode = options.statusCode;
  }
}
