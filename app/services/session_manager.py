class SessionManager:

    def __init__(self):
        self.sessions = {}

    # =========================================================
    # CREATE SESSION
    # =========================================================

    def create_session(
        self,
        session_id: str,
        candidate: dict,
        interview_plan: dict
    ):
        self.sessions[session_id] = {
            "candidate": candidate,
            "interview_plan": interview_plan,
            "conversation": [],
            "question_count": 0,
            "covered_days": [],
            "current_day": None,
            "question_metadata": [],
            "evaluations": [],
            "done": False
        }

        return self.sessions[session_id]

    # =========================================================
    # GET SESSION
    # =========================================================

    def get_session(self, session_id: str):

        return self.sessions.get(session_id)

    # =========================================================
    # ADD MESSAGE
    # =========================================================

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
    ):

        session = self.sessions.get(session_id)

        if not session:
            raise ValueError(
                "Interview session not found."
            )

        session["conversation"].append({
            "role": role,
            "content": content
        })

    # =========================================================
    # QUESTION COUNT
    # =========================================================

    def increment_question_count(
        self,
        session_id: str
    ):

        session = self.sessions.get(session_id)

        if not session:
            raise ValueError(
                "Interview session not found."
            )

        session["question_count"] += 1

    def get_question_count(
        self,
        session_id: str
    ):

        session = self.get_session(
            session_id
        )

        if not session:
            raise ValueError(
                "Interview session not found."
            )

        return session["question_count"]

    # =========================================================
    # CURRICULUM DAYS
    # =========================================================

    def add_covered_day(
        self,
        session_id: str,
        day: int
    ):

        session = self.sessions.get(session_id)

        if not session:
            raise ValueError(
                "Interview session not found."
            )

        if day not in session["covered_days"]:
            session["covered_days"].append(day)

    def get_covered_days(
        self,
        session_id: str
    ):

        session = self.get_session(
            session_id
        )

        if not session:
            raise ValueError(
                "Interview session not found."
            )

        return session["covered_days"]

    # =========================================================
    # CURRENT CURRICULUM DAY
    # =========================================================

    def set_current_day(
        self,
        session_id: str,
        day: int
    ):

        session = self.get_session(
            session_id
        )

        if not session:
            raise ValueError(
                "Interview session not found."
            )

        session["current_day"] = day

    def get_current_day(
        self,
        session_id: str
    ):

        session = self.get_session(
            session_id
        )

        if not session:
            raise ValueError(
                "Interview session not found."
            )

        return session["current_day"]

    # =========================================================
    # QUESTION METADATA
    # =========================================================

    def add_question_metadata(
        self,
        session_id: str,
        metadata: dict
    ):

        session = self.get_session(
            session_id
        )

        if not session:
            raise ValueError(
                "Interview session not found."
            )

        session["question_metadata"].append(
            metadata
        )

    def get_question_metadata(
        self,
        session_id: str
    ):

        session = self.get_session(
            session_id
        )

        if not session:
            raise ValueError(
                "Interview session not found."
            )

        return session["question_metadata"]

    # =========================================================
    # ANSWER EVALUATIONS
    # =========================================================

    def add_evaluation(
        self,
        session_id: str,
        evaluation: dict
    ):

        session = self.get_session(
            session_id
        )

        if not session:
            raise ValueError(
                "Interview session not found."
            )

        session["evaluations"].append(
            evaluation
        )

    def get_evaluations(
        self,
        session_id: str
    ):

        session = self.get_session(
            session_id
        )

        if not session:
            raise ValueError(
                "Interview session not found."
            )

        return session["evaluations"]

    # =========================================================
    # MARK DONE
    # =========================================================

    def mark_done(
        self,
        session_id: str
    ):

        session = self.get_session(
            session_id
        )

        if not session:
            raise ValueError(
                "Interview session not found."
            )

        session["done"] = True

    # =========================================================
    # END SESSION
    # =========================================================

    def end_session(
        self,
        session_id: str
    ):

        session = self.get_session(
            session_id
        )

        if not session:
            raise ValueError(
                "Interview session not found."
            )

        session["done"] = True