from app.services.candidate_profiler import CandidateProfiler
from app.services.curriculum_service import CurriculumService


class InterviewPlanner:

    def __init__(self):
        self.candidate_profiler = CandidateProfiler()
        self.curriculum_service = CurriculumService()

    def create_plan(self, candidate: dict):

        # ---------------------------------------------------------
        # 1. Build candidate profile
        # ---------------------------------------------------------
        profile = self.candidate_profiler.build_profile(candidate)

        completed = profile.get("completed_topics", [])
        needs_practice = profile.get("topics_needing_practice", [])
        strong_topics = profile.get("strong_topics", [])
        skipped_days = set(profile.get("skipped_days", []))

        # ---------------------------------------------------------
        # 2. Normalize skipped curriculum days
        # ---------------------------------------------------------
        normalized_skipped_days = set()

        for day in skipped_days:
            try:
                normalized_skipped_days.add(int(day))
            except (TypeError, ValueError):
                continue

        skipped_days = normalized_skipped_days

        # ---------------------------------------------------------
        # 3. Select topics
        # ---------------------------------------------------------
        selected = []
        selected_day_numbers = set()

        # ---------------------------------------------------------
        # 3A. First priority:
        # Weak / high-attempt topics
        # ---------------------------------------------------------
        for topic in needs_practice:

            try:
                day = int(topic["day"])
            except (TypeError, ValueError, KeyError):
                continue

            if day in skipped_days:
                continue

            if day not in selected_day_numbers:
                selected.append({
                    **topic,
                    "day": day
                })

                selected_day_numbers.add(day)

        # ---------------------------------------------------------
        # 3B. Second priority:
        # Strong topics
        # ---------------------------------------------------------
        for topic in strong_topics:

            try:
                day = int(topic["day"])
            except (TypeError, ValueError, KeyError):
                continue

            if day in skipped_days:
                continue

            if day not in selected_day_numbers:
                selected.append({
                    **topic,
                    "day": day
                })

                selected_day_numbers.add(day)

        # ---------------------------------------------------------
        # 3C. Third priority:
        # Completed topics
        # ---------------------------------------------------------
        for topic in completed:

            try:
                day = int(topic["day"])
            except (TypeError, ValueError, KeyError):
                continue

            if day in skipped_days:
                continue

            if day not in selected_day_numbers:
                selected.append({
                    **topic,
                    "day": day
                })

                selected_day_numbers.add(day)

        # ---------------------------------------------------------
        # 4. Get maximum of 6 candidate-selected days
        # ---------------------------------------------------------
        selected_days = list(selected_day_numbers)[:6]

        # ---------------------------------------------------------
        # 5. Retrieve actual curriculum information
        # ---------------------------------------------------------
        curriculum_topics = []

        for day in selected_days:

            curriculum_day = self.curriculum_service.get_day(day)

            if curriculum_day:

                curriculum_topics.append({
                    "day": day,
                    "title": curriculum_day.get("title"),
                    "type": curriculum_day.get("type"),
                    "tools": curriculum_day.get("tools", []),
                    "objectives": curriculum_day.get("objectives", [])
                })

        # ---------------------------------------------------------
        # 6. Fallback:
        # Make sure we have at least 4 curriculum days
        # ---------------------------------------------------------
        if len(curriculum_topics) < 4:

            for curriculum_day in self.curriculum_service.get_all_days():

                try:
                    day = int(curriculum_day.get("day"))
                except (TypeError, ValueError):
                    continue

                # Don't use skipped days
                if day in skipped_days:
                    continue

                # Don't duplicate already selected days
                if day in selected_day_numbers:
                    continue

                curriculum_topics.append({
                    "day": day,
                    "title": curriculum_day.get("title"),
                    "type": curriculum_day.get("type"),
                    "tools": curriculum_day.get("tools", []),
                    "objectives": curriculum_day.get("objectives", [])
                })

                selected_day_numbers.add(day)

                # We need at least 4 days.
                if len(curriculum_topics) >= 4:
                    break

        # ---------------------------------------------------------
        # 7. Final selected curriculum days
        # ---------------------------------------------------------
        selected_days = [
            topic["day"]
            for topic in curriculum_topics
        ]

        # Limit to maximum 6 days
        selected_days = selected_days[:6]
        curriculum_topics = curriculum_topics[:6]

        # ---------------------------------------------------------
        # 8. DEBUG INFORMATION
        # ---------------------------------------------------------
        print("\n========== INTERVIEW PLAN DEBUG ==========")

        print("Candidate ID:")
        print(profile.get("candidate_id"))

        print("\nCompleted topics:")
        print(completed)

        print("\nTopics needing practice:")
        print(needs_practice)

        print("\nStrong topics:")
        print(strong_topics)

        print("\nSkipped days:")
        print(skipped_days)

        print("\nSelected days:")
        print(selected_days)

        print("\nCurriculum topics:")
        print(curriculum_topics)

        print("==========================================\n")

        # ---------------------------------------------------------
        # 9. Return interview plan
        # ---------------------------------------------------------
        return {
            "candidate": {
                "id": profile["candidate_id"],
                "name": profile["name"],
                "role": profile["job_role"],
                "experience_years": profile["years_experience"]
            },
            "target_days": selected_days,
            "topics": curriculum_topics,
            "minimum_questions": 8,
            "minimum_days": 4
        }