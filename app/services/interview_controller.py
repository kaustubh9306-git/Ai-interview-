class InterviewController:

    MIN_QUESTIONS = 8
    MIN_CURRICULUM_DAYS = 4

    def should_end(
        self,
        question_count: int,
        covered_days: list
    ) -> bool:

        return (
            question_count >= self.MIN_QUESTIONS
            and len(set(covered_days)) >= self.MIN_CURRICULUM_DAYS
        )

    def can_end(
        self,
        question_count: int,
        covered_days: list
    ) -> bool:

        return self.should_end(
            question_count=question_count,
            covered_days=covered_days
        )

    def get_progress(
        self,
        question_count: int,
        covered_days: list
    ) -> dict:

        unique_days = len(set(covered_days))

        return {
            "questions": question_count,
            "required_questions": self.MIN_QUESTIONS,
            "curriculum_days": unique_days,
            "required_curriculum_days": self.MIN_CURRICULUM_DAYS,
            "questions_complete": (
                question_count >= self.MIN_QUESTIONS
            ),
            "curriculum_complete": (
                unique_days >= self.MIN_CURRICULUM_DAYS
            ),
            "complete": self.should_end(
                question_count=question_count,
                covered_days=covered_days
            )
        }