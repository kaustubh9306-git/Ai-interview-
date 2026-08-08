from app.services.candidate_profiler import CandidateProfiler
from app.services.curriculum_service import CurriculumService
from app.services.interview_planner import InterviewPlanner


def test_candidate_loading():

    profiler = CandidateProfiler()

    candidate = profiler.get_candidate("CAND-001")

    assert candidate is not None
    assert candidate["member"]["name"] == "Sarah Johnson"


def test_candidate_profile():

    profiler = CandidateProfiler()

    candidate = profiler.get_candidate("CAND-001")
    profile = profiler.build_profile(candidate)

    assert profile["candidate_id"] == "CAND-001"
    assert len(profile["completed_topics"]) > 0


def test_curriculum_loading():

    curriculum = CurriculumService()

    day = curriculum.get_day(23)

    assert day is not None
    assert day["title"] == "Model Context Protocol (MCP)"

    from app.services.interview_planner import InterviewPlanner


def test_interview_plan():

    profiler = CandidateProfiler()

    candidate = profiler.get_candidate("CAND-001")

    planner = InterviewPlanner()

    plan = planner.create_plan(candidate)

    assert plan["minimum_questions"] == 8
    assert plan["minimum_days"] == 4
    assert len(plan["target_days"]) >= 4
    assert len(plan["topics"]) >= 4