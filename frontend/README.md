# AI Interviewer — Frontend

A focused, adaptive technical-interview workspace built in React + TypeScript
+ Tailwind CSS. This is **frontend only** — it talks to an existing FastAPI
backend and never modifies, mocks, or fakes any backend behavior.

## 1. Prerequisite: the backend must already be running

This frontend does not include or start the backend. Before running it,
start your existing FastAPI backend separately:

```bash
uvicorn app.main:app --reload
```

The backend is expected at `http://127.0.0.1:8000`, with docs available at
`http://127.0.0.1:8000/docs`.

## 2. Frontend setup

```bash
npm install
cp .env.example .env   # optional — defaults already point at the backend above
npm run dev
```

The frontend runs at `http://localhost:5173`.

## 3. Environment variable

| Variable            | Default                 | Purpose                                          |
|----------------------|--------------------------|---------------------------------------------------|
| `VITE_API_BASE_URL` | `http://127.0.0.1:8000` | Base URL the frontend calls for `/api/interview` |

Set this in `.env` if your backend runs somewhere other than the default.

## 4. How the frontend talks to the API

All HTTP logic lives in `src/services/interviewApi.ts` — no component makes
a raw `fetch` call. There is exactly one backend endpoint in use:

```
POST /api/interview
```

**Starting an interview** (candidate required, once):

```json
{ "sessionId": "<generated UUID>", "candidate": { "member": { ... } } }
```

**Submitting an answer** (same sessionId reused for the rest of the session):

```json
{ "sessionId": "<same UUID>", "message": "<candidate's answer>" }
```

**Every response** — this is the full, real contract; the frontend does not
assume any field beyond these two:

```json
{ "reply": "string", "done": false }
```

When `done` is `true`, the app shows the completion screen using only
`reply` and the number of questions actually asked during the session — no
fabricated scores, topics, or progress fractions.

## 5. Interview flow

```
Landing screen → review demo candidate → Start Interview
  → sessionId generated (crypto.randomUUID())
  → POST candidate + sessionId → first question displayed
  → candidate answers → POST message + sessionId → next question
  → repeat until done: true → completion screen → Start New Interview
```

State transitions are modeled explicitly in `src/hooks/useInterview.ts`:
`IDLE → STARTING → QUESTION ⇄ SUBMITTING → COMPLETED`, with `ERROR` reachable
from any in-flight request and a retry that resumes without losing the
session.

## 6. Project structure

```
src/
├── components/     Reusable UI (QuestionCard, AnswerComposer, SessionRail, …)
├── pages/          LandingPage, InterviewPage
├── services/       interviewApi.ts — the only place fetch() is called
├── hooks/          useInterview.ts — the interview state machine
├── types/          interview.ts — Candidate / request / response types
└── config/         demoCandidate.ts — frontend-only demo payload
```

## 7. Known limitation

Because the backend currently returns only `{ reply, done }`, the UI cannot
show a real progress fraction, current curriculum topic, or a score. The
"Interview log" panel and question counter are derived entirely from the
number of exchanges that actually happened on the frontend — they are not
backend-reported values. If the backend contract is later extended (e.g. a
`topic` or `score` field), extend `InterviewResponse` in
`src/types/interview.ts` and the relevant display component — no other
files need to change.
