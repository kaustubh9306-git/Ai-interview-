# ABTalks AI Interview Agent — Prompt Submission

## Project Title
ABTalks AI Interview Agent

## One-Line Description
An adaptive AI-powered technical interview platform that generates interview questions, evaluates candidate answers, and produces structured post-interview feedback.

## Problem Statement
Traditional interview-practice tools often rely on fixed question lists and provide limited actionable feedback. Candidates need a realistic interview experience where questions adapt to previous answers and where their performance is evaluated across technical concepts.

## Proposed Solution
ABTalks AI Interview Agent provides a complete interview workflow:

1. Candidate starts an interview session.
2. The FastAPI backend creates an interview plan using candidate information and curriculum data.
3. An AI interview agent generates questions based on the candidate, curriculum, covered topics, and previous answers.
4. The candidate answers through the React frontend.
5. The backend evaluates each answer.
6. The next question is generated based on the evaluation and current interview state.
7. The controller determines when the interview is complete.
8. A final feedback dashboard presents the candidate's score, strengths, technical gaps, and recommended next steps.

## Key Features

### Adaptive Questioning
Questions are generated dynamically rather than following a completely fixed script. The interview agent considers the candidate profile, interview plan, conversation history, covered curriculum days, and answer evaluations.

### Structured Answer Evaluation
Candidate responses are evaluated by a dedicated answer-evaluation service. The evaluation contributes to the final technical assessment and identifies strengths and areas requiring improvement.

### Session-Based Interview Management
Each interview receives a unique session ID. The backend stores the conversation, question metadata, current curriculum day, covered topics, question count, and completion state.

### Curriculum-Aware Interview Planning
The interview planner selects relevant curriculum topics based on the candidate's existing progress, completed topics, practice needs, and strong topics.

### Final Performance Dashboard
After completion, the frontend displays:
- Technical score
- Number of questions evaluated
- Interview summary
- Strengths
- Areas to improve
- Recommended next steps

## Technology Stack

### Backend
- Python
- FastAPI
- Pydantic
- Uvicorn
- Modular service architecture

### Frontend
- React
- TypeScript / JSX
- Vite
- Tailwind CSS
- Lucide React

### Testing
- Pytest

## Architecture

```text
Candidate
    |
    v
React Frontend
    |
    | POST /api/interview
    v
FastAPI
    |
    +--> CandidateProfiler
    |
    +--> InterviewPlanner
    |
    +--> InterviewAgent
    |
    +--> SessionManager
    |
    +--> AnswerEvaluator
    |
    +--> InterviewController
    |
    v
Interview Response
    |
    +--> Next Question
    |
    +--> Final Feedback
    |
    v
React Interview UI
    |
    v
Performance Dashboard
```

## Backend API Contract

### Start Interview

```http
POST /api/interview
Content-Type: application/json
```

Request:

```json
{
  "sessionId": "unique-session-id",
  "candidate": {
    "member": {
      "id": "CAND-007",
      "name": "Candidate",
      "jobRole": "AI Engineer",
      "yearsExperience": 1,
      "education": "Engineering",
      "status": "active"
    }
  }
}
```

### Submit Answer

```http
POST /api/interview
Content-Type: application/json
```

Request:

```json
{
  "sessionId": "unique-session-id",
  "message": "Candidate answer"
}
```

### During Interview

```json
{
  "reply": "Next interview question",
  "done": false
}
```

### After Completion

```json
{
  "reply": "Interview completed.",
  "done": true,
  "feedback": {
    "summary": "Interview completed with an average technical score of 8.0/10.",
    "average_score": 8.0,
    "total_questions": 8,
    "strengths": [
      "Strong technical understanding"
    ],
    "gaps": [
      "Needs more depth in system design"
    ],
    "next": [
      "Practice practical AI engineering scenarios."
    ]
  }
}
```

## Validation and Testing

The backend test suite currently validates the core services and interview workflow.

The completed test run produced:

```text
12 passed in 8.40s
```

The validated areas include:

- Candidate loading
- Candidate profiling
- Curriculum loading
- Interview planning
- Answer evaluation
- Interview agent
- Interview completion controller
- Session creation
- Session messages
- Question counting

## Example Final Interview Result

A completed interview successfully produced:

```text
Technical Score: 8/10
Questions Evaluated: 8
```

The dashboard also displayed the generated:
- Interview summary
- Strengths
- Areas to improve
- Recommended next steps

## Why This Project Is Different

The goal is not to build another chatbot that simply asks predefined questions.

The system separates the interview workflow into specialized components:

- Candidate profiling
- Curriculum planning
- Question generation
- Answer evaluation
- Session management
- Interview completion control
- Feedback generation

This allows the interview experience to behave more like a structured technical interview rather than a generic conversational AI application.

## Future Improvements

Potential extensions include:

- Competency-wise score breakdown
- Visual performance analytics
- Topic coverage visualization
- Difficulty progression
- Voice-based interviewing
- Resume-aware questioning
- Interview history and comparison
- Personalized learning recommendations
- Deployment with production authentication and database persistence

## Submission Note

This document describes the implemented project architecture, workflow, API contract, testing status, and final user-facing result. It can be submitted alongside the source repository when the hackathon requires a project/prompt description document.
