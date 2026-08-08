import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class AnswerEvaluator:

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

    def evaluate(
        self,
        question: str,
        answer: str,
        curriculum_topic: str = ""
    ) -> dict:

        system_prompt = """
You are a strict but fair technical interview evaluator.

Evaluate the candidate's answer based ONLY on the
question and answer provided.

Do not assume knowledge that the candidate did not demonstrate.

Evaluate:

1. Technical correctness
2. Depth of understanding
3. Engineering reasoning
4. Clarity

Return ONLY valid JSON:

{
    "score": 0,
    "technical_correctness": 0,
    "depth": 0,
    "reasoning": 0,
    "clarity": 0,
    "strengths": [],
    "gaps": [],
    "follow_up_needed": true,
    "follow_up_reason": "string"
}

All scores must be integers from 0 to 10.

Be strict.

A vague answer should receive a lower score.

A technically incorrect answer should receive a low
technical correctness score.

Do not reward claims that are not supported by the answer.
"""

        user_prompt = f"""
Curriculum topic:
{curriculum_topic}

Interview question:
{question}

Candidate answer:
{answer}

Evaluate this answer.
"""

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
            temperature=0.1,
            max_tokens=500
        )

        raw_output = (
            response.choices[0]
            .message
            .content
            .strip()
        )

        try:

            result = json.loads(raw_output)

        except json.JSONDecodeError:

            start = raw_output.find("{")
            end = raw_output.rfind("}")

            if start == -1 or end == -1:
                raise ValueError(
                    "LLM evaluator did not return valid JSON."
                )

            result = json.loads(
                raw_output[start:end + 1]
            )

        # -------------------------------------------------
        # Validate score
        # -------------------------------------------------

        result["score"] = max(
            0,
            min(
                10,
                int(result.get("score", 0))
            )
        )

        for field in [
            "technical_correctness",
            "depth",
            "reasoning",
            "clarity"
        ]:

            result[field] = max(
                0,
                min(
                    10,
                    int(result.get(field, 0))
                )
            )

        result.setdefault(
            "strengths",
            []
        )

        result.setdefault(
            "gaps",
            []
        )

        result.setdefault(
            "follow_up_needed",
            False
        )

        result.setdefault(
            "follow_up_reason",
            ""
        )

        return result