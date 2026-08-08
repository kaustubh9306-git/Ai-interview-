from app.services.session_manager import SessionManager


def test_session_creation():

    manager = SessionManager()

    session = manager.create_session(
        session_id="test-123",
        candidate={
            "name": "Test Candidate"
        },
        interview_plan={
            "target_days": [8, 10, 12, 23]
        }
    )

    assert session["candidate"]["name"] == "Test Candidate"
    assert session["question_count"] == 0
    assert session["conversation"] == []
    assert session["done"] is False


def test_session_messages():

    manager = SessionManager()

    manager.create_session(
        session_id="test-123",
        candidate={},
        interview_plan={}
    )

    manager.add_message(
        "test-123",
        "assistant",
        "Explain RAG."
    )

    manager.add_message(
        "test-123",
        "user",
        "RAG retrieves relevant documents."
    )

    session = manager.get_session("test-123")

    assert len(session["conversation"]) == 2


def test_question_count():

    manager = SessionManager()

    manager.create_session(
        session_id="test-123",
        candidate={},
        interview_plan={}
    )

    manager.increment_question_count("test-123")
    manager.increment_question_count("test-123")

    session = manager.get_session("test-123")

    assert session["question_count"] == 2