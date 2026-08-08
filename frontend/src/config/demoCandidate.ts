import type { Candidate } from "../types/interview";

/**
 * Frontend-only demo candidate used to start an interview during the
 * hackathon demo. This is NOT written to or read from the backend's
 * candidates.json — it exists solely as the payload the current API
 * requires when starting a new session.
 */
export const DEMO_CANDIDATE: Candidate = {
  member: {
    id: "CAND-007",
    name: "Demo Candidate",
    jobRole: "AI Engineer",
    yearsExperience: 2,
    education: "Computer Science",
    status: "active",
  },
};
