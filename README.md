# AI Interview Agent

An adaptive AI-powered technical interviewer that conducts personalized,
multi-turn interviews based on a candidate's learning journey.

The system uses the candidate's completed curriculum, learning signals,
previous answers, and interview context to dynamically generate technical
questions, ask follow-ups, evaluate responses, and generate actionable
feedback.

---

## Problem Statement

Traditional technical interview preparation often relies on static question
banks.

This creates several problems:

- Questions are not personalized to the candidate.
- Weak areas are not explored deeply.
- Follow-up questions are usually missing.
- The interview does not adapt to previous answers.
- Feedback is often generic rather than actionable.

The **AI Interview Agent** addresses this by behaving more like a real
technical interviewer.

Instead of simply asking predefined questions, the agent:

1. Builds an interview plan from the candidate's learning journey.
2. Selects relevant curriculum topics.
3. Conducts a multi-turn technical interview.
4. Maintains conversation context.
5. Evaluates candidate responses.
6. Generates intelligent follow-up questions.
7. Produces structured feedback at the end.

---

# Key Features

### Personalized Interview Planning

The system analyzes:

- Candidate profile
- Completed missions
- Attempt history
- Skipped topics
- Learning signals
- Curriculum coverage

and creates a personalized interview plan.

### Adaptive Question Generation

Questions are generated dynamically using the candidate's:

- Current topic
- Previous answers
- Interview history
- Demonstrated knowledge

The agent can increase or decrease difficulty based on performance.

### Conversational Follow-ups

The interviewer does not blindly move from one question to another.

It can identify weaknesses or incomplete explanations and ask targeted
follow-up questions.

Example:

```text
Interviewer:
Explain how vector databases are used in RAG.

Candidate:
They store embeddings and retrieve similar documents.

Interviewer:
You mentioned similarity search. Why would cosine similarity
be useful when comparing embeddings?
```