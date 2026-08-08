from app.services.interview_controller import InterviewController


def test_interview_not_complete_early():

    controller = InterviewController()

    assert controller.should_end(
        question_count=5,
        covered_days=[8, 10, 12, 23]
    ) is False


def test_interview_requires_four_days():

    controller = InterviewController()

    assert controller.should_end(
        question_count=8,
        covered_days=[8, 10, 12]
    ) is False


def test_interview_complete():

    controller = InterviewController()

    assert controller.should_end(
        question_count=8,
        covered_days=[8, 10, 12, 23]
    ) is True