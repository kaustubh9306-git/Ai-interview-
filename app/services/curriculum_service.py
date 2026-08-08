from app.services.data_loader import load_curriculum


class CurriculumService:

    def __init__(self):
        self.curriculum = load_curriculum()
        self.days = self.curriculum.get("days", [])
        self.modules = self.curriculum.get("modules", [])

    def get_all_days(self):
        return self.days

    def get_day(self, day_number):
        """
        Get a curriculum day regardless of whether
        day_number is passed as int or string.
        """
        try:
            day_number = int(day_number)
        except (TypeError, ValueError):
            return None

        for day in self.days:
            try:
                if int(day.get("day")) == day_number:
                    return day
            except (TypeError, ValueError):
                continue

        return None

    def get_days(self, day_numbers):
        """
        Get multiple curriculum days while safely
        handling string/int day numbers.
        """
        normalized_days = set()

        for day_number in day_numbers:
            try:
                normalized_days.add(int(day_number))
            except (TypeError, ValueError):
                continue

        return [
            day for day in self.days
            if day.get("day") in normalized_days
        ]

    def get_module_for_day(self, day_number):
        try:
            day_number = int(day_number)
        except (TypeError, ValueError):
            return None

        for module in self.modules:
            if day_number in module.get("days", []):
                return module

        return None