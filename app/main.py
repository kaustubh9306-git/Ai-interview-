from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from app.services.candidate_profiler import CandidateProfiler
from app.services.interview_planner import InterviewPlanner
from app.services.interview_agent import InterviewAgent
from app.services.answer_evaluator import AnswerEvaluator
from app.services.session_manager import SessionManager
from app.services.interview_controller import InterviewController


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="ABTalks AI Interview Agent",
    version="1.0.0"
)


# ============================================================
# CORS
# Allows the React/Vite frontend to communicate with FastAPI
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# SERVICES
# ============================================================

candidate_profiler = CandidateProfiler()
interview_planner = InterviewPlanner()
interview_agent = InterviewAgent()
answer_evaluator = AnswerEvaluator()
session_manager = SessionManager()
interview_controller = InterviewController()


# ============================================================
# REQUEST MODEL
# ============================================================

class InterviewRequest(BaseModel):
    sessionId: str
    candidate: Optional[dict] = None
    message: Optional[str] = None


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "ABTalks AI Interview Agent is running"
    }


# ============================================================
# INTERVIEW ENDPOINT
# ============================================================

@app.post("/api/interview")
def interview(request: InterviewRequest):

    # --------------------------------------------------------
    # Check whether session already exists
    # --------------------------------------------------------

    session = session_manager.get_session(
        request.sessionId
    )

    # ========================================================
    # START NEW INTERVIEW
    # ========================================================

    if session is None:

        if request.candidate is None:
            raise HTTPException(
                status_code=400,
                detail="candidate is required when starting an interview"
            )

        try:

            # ------------------------------------------------
            # Resolve candidate
            # ------------------------------------------------

            candidate_data = request.candidate

            if (
                isinstance(candidate_data, dict)
                and "id" in candidate_data
                and len(candidate_data) == 1
            ):

                candidate_id = candidate_data["id"]

                candidate_data = candidate_profiler.get_candidate(
                    candidate_id
                )

                if candidate_data is None:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Candidate {candidate_id} not found"
                    )

            # ------------------------------------------------
            # Create interview plan
            # ------------------------------------------------

            plan = interview_planner.create_plan(
                candidate_data
            )

            if not plan:
                raise ValueError(
                    "Interview planner returned an empty plan."
                )

            # ------------------------------------------------
            # Create session
            # ------------------------------------------------

            session = session_manager.create_session(
                session_id=request.sessionId,
                candidate=candidate_data,
                interview_plan=plan
            )

            # ------------------------------------------------
            # Generate first question
            # ------------------------------------------------

            decision = interview_agent.generate_question(
                candidate=candidate_data,
                interview_plan=plan,
                conversation=[],
                covered_days=[]
            )

            # ------------------------------------------------
            # Store first question
            # ------------------------------------------------

            session_manager.add_message(
                request.sessionId,
                "assistant",
                decision["question"]
            )

            session_manager.increment_question_count(
                request.sessionId
            )

            session_manager.set_current_day(
                request.sessionId,
                decision["curriculum_day"]
            )

            session_manager.add_covered_day(
                request.sessionId,
                decision["curriculum_day"]
            )

            session_manager.add_question_metadata(
                request.sessionId,
                decision
            )

            # ------------------------------------------------
            # Return first question
            # ------------------------------------------------

            return {
                "reply": decision["question"],
                "done": False
            }

        except HTTPException:
            raise

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

    # ========================================================
    # INTERVIEW ALREADY COMPLETED
    # ========================================================

    if session["done"]:

        return {
            "reply": "Interview has already been completed.",
            "done": True
        }

    # ========================================================
    # ONGOING INTERVIEW
    # ========================================================

    if not request.message:

        raise HTTPException(
            status_code=400,
            detail="message is required for an ongoing interview"
        )

    # --------------------------------------------------------
    # Get the previous question
    # --------------------------------------------------------

    previous_question = ""

    if session["question_metadata"]:

        previous_question = session[
            "question_metadata"
        ][-1].get(
            "question",
            ""
        )

    # --------------------------------------------------------
    # Get current curriculum day
    # --------------------------------------------------------

    current_day = session.get(
        "current_day"
    )

    # --------------------------------------------------------
    # Get curriculum topic
    # --------------------------------------------------------

    curriculum_topic = ""

    for topic in session["interview_plan"].get(
        "topics",
        []
    ):

        if (
            isinstance(topic, dict)
            and topic.get("day") == current_day
        ):

            curriculum_topic = topic.get(
                "title",
                ""
            )

            break

    # --------------------------------------------------------
    # Store candidate answer
    # --------------------------------------------------------

    session_manager.add_message(
        request.sessionId,
        "user",
        request.message
    )

    # ========================================================
    # EVALUATE CANDIDATE ANSWER
    # ========================================================

    try:

        evaluation = answer_evaluator.evaluate(
            question=previous_question,
            answer=request.message,
            curriculum_topic=curriculum_topic
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Answer evaluation failed: {str(e)}"
        )

    # --------------------------------------------------------
    # Store evaluation in question metadata
    # --------------------------------------------------------

    session["question_metadata"][-1][
        "evaluation"
    ] = evaluation

    # ========================================================
    # GET CURRENT INTERVIEW STATE
    # ========================================================

    current_question_count = (
        session_manager.get_question_count(
            request.sessionId
        )
    )

    covered_days = (
        session_manager.get_covered_days(
            request.sessionId
        )
    )

    # ========================================================
    # CHECK WHETHER INTERVIEW SHOULD END
    # ========================================================

    if interview_controller.should_end(
        question_count=current_question_count,
        covered_days=covered_days
    ):

        session_manager.mark_done(
            request.sessionId
        )

        # ----------------------------------------------------
        # Build final feedback
        # ----------------------------------------------------

        all_evaluations = []

        for metadata in session[
            "question_metadata"
        ]:

            if "evaluation" in metadata:
                all_evaluations.append(
                    metadata["evaluation"]
                )

        strengths = []
        gaps = []

        for result in all_evaluations:

            for item in result.get(
                "strengths",
                []
            ):

                if item not in strengths:
                    strengths.append(item)

            for item in result.get(
                "gaps",
                []
            ):

                if item not in gaps:
                    gaps.append(item)

        average_score = 0

        if all_evaluations:

            total_score = sum(
                result.get(
                    "score",
                    0
                )
                for result in all_evaluations
            )

            average_score = round(
                total_score / len(all_evaluations),
                1
            )

        return {
    "reply": "Interview completed.",
    "done": True,
    "feedback": {
        "summary": (
            f"Interview completed with an "
            f"average technical score of "
            f"{average_score}/10."
        ),
        "average_score": average_score,
        "total_questions": len(all_evaluations),
        "strengths": strengths[:5],
        "gaps": gaps[:5],
        "next": [
            "Review the identified technical gaps.",
            "Practice explaining engineering decisions clearly.",
            "Work through practical AI engineering scenarios."
        ]
    }
}

    # ========================================================
    # GENERATE NEXT QUESTION
    # ========================================================

    try:

        decision = interview_agent.generate_question(
            candidate=session["candidate"],
            interview_plan=session["interview_plan"],
            conversation=session["conversation"],
            covered_days=session["covered_days"],
            evaluation=evaluation
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Question generation failed: {str(e)}"
        )

    # ========================================================
    # STORE NEXT QUESTION
    # ========================================================

    session_manager.add_message(
        request.sessionId,
        "assistant",
        decision["question"]
    )

    session_manager.increment_question_count(
        request.sessionId
    )

    session_manager.set_current_day(
        request.sessionId,
        decision["curriculum_day"]
    )

    session_manager.add_covered_day(
        request.sessionId,
        decision["curriculum_day"]
    )

    session_manager.add_question_metadata(
        request.sessionId,
        decision
    )

    # ========================================================
    # RETURN NEXT QUESTION
    # ========================================================

    return {
        "reply": decision["question"],
        "done": False
    }