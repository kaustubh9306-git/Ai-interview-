from app.services.interview_agent import InterviewAgent


def test_interview_agent():

    agent = InterviewAgent()

    candidate = {
        "name": "Test Candidate",
        "role": "AI Engineer"
    }

    interview_plan = {
        "target_days": [8, 10, 12, 23],
        "topics": [
            {
                "day": 8,
                "title": "Vector Databases"
            },
            {
                "day": 10,
                "title": "Retrieval"
            },
            {
                "day": 12,
                "title": "Prompt Engineering"
            },
            {
                "day": 23,
                "title": "MCP"
            }
        ]
    }

    conversation = []

    question = agent.generate_question(
        candidate=candidate,
        interview_plan=interview_plan,
        conversation=conversation,
        covered_days=[]
    )

    assert isinstance(question, dict)

    assert "question" in question
    assert "curriculum_day" in question
    assert "difficulty" in question
    assert "intent" in question

    assert isinstance(question["question"], str)
    assert len(question["question"].strip()) > 0

    assert question["curriculum_day"] in [8, 10, 12, 23]

    assert question["difficulty"] in [
        "easy",
        "medium",
        "hard"
    ]

    assert question["intent"] in [
        "initial",
        "follow_up",
        "deeper_probe",
        "topic_transition"
    ]