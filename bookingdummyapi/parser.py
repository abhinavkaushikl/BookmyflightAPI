# booking_logic/parser.py

import re
from datetime import datetime, timedelta

class TravelQueryParser:
    def __init__(self):
        self.default_destination = "Unknown"
        self.default_preference = "beach"
        self.default_trip_duration_days = 3
        self.preference_keywords = ["beach", "mountain", "lake", "city", "forest", "desert", "island"]

    def parse(self, text: str) -> dict:
        destination = self._extract_destination(text)
        preferences = self._extract_preference(text)
        trip_duration = self._extract_duration(text)
        departure_date, return_date = self._calculate_dates(text, trip_duration)

        return {
            "destination": destination,
            "departure_date": departure_date,
            "return_date": return_date,
            "preferences": preferences
        }

    def _extract_destination(self, text: str) -> str:
        match = re.search(r"(?:to|in|for)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)", text)
        return match.group(1) if match else self.default_destination

    def _extract_preference(self, text: str) -> str:
        for keyword in self.preference_keywords:
            if keyword in text.lower():
                return keyword
        return self.default_preference

    def _extract_duration(self, text: str) -> int:
        match = re.search(r"(\d+)\s*(?:days|day)", text.lower())
        if match:
            return int(match.group(1))
        return self.default_trip_duration_days

    def _calculate_dates(self, text: str, trip_duration_days: int):
        today = datetime.today()
        if "weekend" in text.lower():
            days_until_saturday = (5 - today.weekday()) % 7
            departure = today + timedelta(days=days_until_saturday)
        else:
            departure = today + timedelta(days=2)
        return_date = departure + timedelta(days=trip_duration_days)
        return departure.strftime("%Y-%m-%d"), return_date.strftime("%Y-%m-%d")


if __name__ == "__main__":
    print("TravelQueryParser CLI")
    parser = TravelQueryParser()
    while True:
        user_input = input("\nEnter travel query (or 'exit'): ")
        if user_input.lower() == 'exit':
            break
        parsed_info = parser.parse(user_input)
        print("Parsed Info:", parsed_info)
