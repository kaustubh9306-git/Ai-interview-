from app.services.data_loader import load_candidates


class CandidateProfiler:

    def __init__(self):
        data = load_candidates()
        self.candidates = data.get("candidates", [])

    def get_candidate(self, candidate_id: str):
        for candidate in self.candidates:
            member = candidate.get("member", {})

            if member.get("id") == candidate_id:
                return candidate

        return None

    def build_profile(self, candidate: dict):
        member = candidate.get("member", {})
        missions = candidate.get("missions", [])
        signals = candidate.get("signals", {})

        completed = []
        skipped = []
        attempts = {}

        for mission in missions:
            day = mission.get("day")
            title = mission.get("title")

            if mission.get("skipped"):
                skipped.append({
                    "day": day,
                    "title": title
                })

            elif mission.get("passed"):
                completed.append({
                    "day": day,
                    "title": title,
                    "attempts": mission.get("attempts", 0)
                })

                attempts[day] = mission.get("attempts", 0)

        strong_topics = [
            item for item in completed
            if item["attempts"] <= 2
        ]

        topics_needing_practice = [
            item for item in completed
            if item["attempts"] >= 4
        ]

        return {
            "candidate_id": member.get("id"),
            "name": member.get("name"),
            "job_role": member.get("jobRole"),
            "years_experience": member.get("yearsExperience"),
            "education": member.get("education"),
            "status": member.get("status"),

            "completed_topics": completed,

            "skipped_topics": skipped,

            "strong_topics": strong_topics,

            "topics_needing_practice": topics_needing_practice,

            "signals": signals,

            "completed_days": [
                item["day"] for item in completed
            ],

            "skipped_days": [
                item["day"] for item in skipped
            ]
        }