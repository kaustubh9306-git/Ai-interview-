import json
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class InterviewAgent:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not set in the environment."
            )

        self.client = Groq(api_key=api_key)

        self.model = os.getenv(
            "GROQ_MODEL",
            "llama-3.1-8b-instant"
        )

    # =========================================================
    # GET VALID CURRICULUM DAYS
    # =========================================================

    def _get_valid_days(self, interview_plan: dict) -> list[int]:

        valid_days = []

        for item in interview_plan.get("topics", []):

            if not isinstance(item, dict):
                continue

            day = item.get("day")

            if isinstance(day, int):
                valid_days.append(day)

        return list(dict.fromkeys(valid_days))

    # =========================================================
    # GET TOPIC FOR DAY
    # =========================================================

    def _get_topic_for_day(
        self,
        interview_plan: dict,
        day: int
    ) -> dict:

        for item in interview_plan.get("topics", []):

            if (
                isinstance(item, dict)
                and item.get("day") == day
            ):
                return item

        return {
            "day": day,
            "title": "Technical Topic"
        }

    # =========================================================
    # SELECT NEXT DAY
    # =========================================================

    def select_next_day(
        self,
        interview_plan: dict,
        covered_days: list
    ) -> int:

        valid_days = self._get_valid_days(
            interview_plan
        )

        if not valid_days:
            raise ValueError(
                "No curriculum days available."
            )

        covered = set(covered_days)

        # First cover topics that haven't been covered yet
        for day in valid_days:

            if day not in covered:
                return day

        # If all topics are covered, cycle through them
        index = len(covered_days) % len(valid_days)

        return valid_days[index]

    # =========================================================
    # GENERATE QUESTION
    # =========================================================

    def generate_question(
        self,
        candidate: dict,
        interview_plan: dict,
        conversation: list,
        covered_days: list,
        evaluation: dict | None = None
    ) -> dict:

        # -----------------------------------------------------
        # Validate curriculum
        # -----------------------------------------------------

        valid_days = self._get_valid_days(
            interview_plan
        )

        if not valid_days:
            raise ValueError(
                "No valid curriculum days found in interview plan."
            )

        # -----------------------------------------------------
        # Select next curriculum day
        # -----------------------------------------------------

        next_day = self.select_next_day(
            interview_plan=interview_plan,
            covered_days=covered_days
        )

        topic = self._get_topic_for_day(
            interview_plan=interview_plan,
            day=next_day
        )

        topic_title = topic.get(
            "title",
            "Technical Topic"
        )

        # -----------------------------------------------------
        # Determine intent
        # -----------------------------------------------------

        if not conversation:
            intent = "initial"
        else:
            intent = "follow_up"

        # -----------------------------------------------------
        # Conversation context
        # -----------------------------------------------------

        recent_conversation = conversation[-8:]

        conversation_text = ""

        for message in recent_conversation:

            if not isinstance(message, dict):
                continue

            role = message.get(
                "role",
                "unknown"
            )

            content = message.get(
                "content",
                ""
            )

            conversation_text += (
                f"{role.upper()}: {content}\n"
            )

        # -----------------------------------------------------
        # Candidate information
        # -----------------------------------------------------

        candidate_text = json.dumps(
            candidate,
            indent=2,
            default=str
        )

        # -----------------------------------------------------
        # Evaluation information
        # -----------------------------------------------------

        evaluation_text = ""

        if evaluation:

            evaluation_text = f"""
Previous candidate answer evaluation:

{json.dumps(evaluation, indent=2, default=str)}

Use this evaluation when generating the next question.

If the candidate has significant gaps:
- ask a follow-up question that probes those gaps.

If the candidate demonstrated strong understanding:
- increase difficulty or ask a deeper engineering question.

If follow_up_needed is true:
- prioritize a meaningful follow-up.

Do not simply repeat the previous question.
"""

        # -----------------------------------------------------
        # System prompt
        # -----------------------------------------------------

        system_prompt = """
You are a senior technical interviewer conducting a
realistic AI engineering interview.

Your job is NOT to conduct a scripted quiz.

You must:

1. Ask technically meaningful questions.
2. Personalize questions using the candidate profile.
3. Maintain conversation context.
4. Ask follow-up questions when appropriate.
5. Test understanding rather than memorization.
6. Probe engineering decisions and trade-offs.
7. Gradually increase difficulty when the candidate performs well.
8. Identify gaps in understanding.
9. Keep the interview conversational.

The application controls the curriculum day.

You MUST use the supplied preferred curriculum day.

Do NOT invent a curriculum day.

Return ONLY valid JSON in this format:

{
    "question": "string",
    "curriculum_day": integer,
    "difficulty": "easy|medium|hard",
    "intent": "initial|follow_up|deep_dive|scenario"
}

Do not include markdown.
Do not include explanations outside the JSON.
"""

        # -----------------------------------------------------
        # User prompt
        # -----------------------------------------------------

        user_prompt = f"""
Candidate profile:

{candidate_text}

Interview plan:

{json.dumps(interview_plan, indent=2, default=str)}

Previously covered curriculum days:

{json.dumps(covered_days)}

Preferred next curriculum day:

{next_day}

Preferred topic:

{topic_title}

Previous conversation:

{conversation_text}

Interview intent:

{intent}

{evaluation_text}

Generate the next technical interview question.

The question MUST relate to curriculum day {next_day}.

The curriculum_day in the JSON response MUST be:

{next_day}

If there is a previous candidate answer, use it to
create a meaningful follow-up or deeper question where
appropriate.

Avoid repeating an identical question.

Test practical understanding, engineering reasoning,
trade-offs, architecture or implementation decisions
where appropriate.
"""

        # -----------------------------------------------------
        # Call Groq
        # -----------------------------------------------------

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.3,
            max_tokens=400
        )

        raw_output = (
            response.choices[0]
            .message
            .content
            .strip()
        )

        # -----------------------------------------------------
        # Parse JSON
        # -----------------------------------------------------

        try:

            decision = json.loads(
                raw_output
            )

        except json.JSONDecodeError:

            start = raw_output.find("{")
            end = raw_output.rfind("}")

            if start == -1 or end == -1:
                raise ValueError(
                    "LLM did not return valid JSON."
                )

            try:

                decision = json.loads(
                    raw_output[start:end + 1]
                )

            except json.JSONDecodeError as exc:

                raise ValueError(
                    "Unable to parse LLM response as JSON."
                ) from exc

        # -----------------------------------------------------
        # Validate question
        # -----------------------------------------------------

        question = decision.get(
            "question"
        )

        if not isinstance(question, str):
            raise ValueError(
                "LLM response does not contain a valid question."
            )

        # -----------------------------------------------------
        # Application controls curriculum day
        # -----------------------------------------------------

        decision["curriculum_day"] = next_day

        # -----------------------------------------------------
        # Validate difficulty
        # -----------------------------------------------------

        difficulty = decision.get(
            "difficulty",
            "medium"
        )

        if difficulty not in {
            "easy",
            "medium",
            "hard"
        }:

            difficulty = "medium"

        decision["difficulty"] = difficulty

        # -----------------------------------------------------
        # Validate intent
        # -----------------------------------------------------

        intent_value = decision.get(
            "intent",
            intent
        )

        allowed_intents = {
            "initial",
            "follow_up",
            "deep_dive",
            "scenario"
        }

        if intent_value not in allowed_intents:

            intent_value = intent

        decision["intent"] = intent_value

        # -----------------------------------------------------
        # Return final question decision
        # -----------------------------------------------------

        return decision