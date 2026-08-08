from typing import Optional
from pydantic import BaseModel, Field


class Candidate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    experience_years: Optional[float] = None


class Feedback(BaseModel):
    summary: str
    strengths: list[str]
    gaps: list[str]
    next: list[str]


class InterviewRequest(BaseModel):
    sessionId: str = Field(..., min_length=1)
    candidate: Optional[dict] = None
    message: Optional[str] = None


class InterviewResponse(BaseModel):
    reply: str
    done: bool
    feedback: Optional[Feedback] = None