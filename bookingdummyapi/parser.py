import re
from datetime import datetime, timedelta
import spacy
import dateparser  # pip install dateparser
from difflib import get_close_matches

nlp = spacy.load("en_core_web_trf")

# For demonstration, a small sample city list
CITY_LIST = ["Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Jaipur", "Ahmedabad","Paris", "London", "New York", "Tokyo", "Sydney", "Dubai"]

class TravelQueryParser:
    def __init__(self):
        self.default_preference = "beach"
        self.preference_keywords = ["beach", "mountain", "lake", "city", "forest", "desert", "island"]
        self.default_trip_days = 3
        self.stopwords = {"book", "travel", "trip", "want", "date", "will", "be", "and", "i", "prefer", "prefered"}

    def parse(self, text: str) -> dict:
        destination = self._extract_city(text)
        departure_date, return_date = self._extract_dates(text)
        preference = self._extract_preference(text)
        return {
            "destination": destination,
            "departure_date": departure_date,
            "return_date": return_date,
            "preferences": preference
        }

    def _extract_city(self, text: str) -> str:
        # First: spaCy NER for GPE
        doc = nlp(text)
        cities_found = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

        # Check if spaCy found valid city in our city list (fuzzy match)
        for city in cities_found:
            best_match = self._fuzzy_city_match(city)
            if best_match:
                return best_match

        # Fallback: look for city names after prepositions with fuzzy matching
        prepositions = ["to", "in", "for", "at", "from"]
        text_lower = text.lower()
        for prep in prepositions:
            pattern = rf"{prep}\s+([a-z\s]+)"
            matches = re.findall(pattern, text_lower)
            for match in matches:
                # filter stopwords and check city name similarity
                words = match.split()
                filtered_words = [w for w in words if w not in self.stopwords]
                candidate = " ".join(filtered_words).title()
                best_match = self._fuzzy_city_match(candidate)
                if best_match:
                    return best_match

        return "Unknown"

    def _fuzzy_city_match(self, word: str) -> str or None:
        # Return closest city from CITY_LIST with similarity threshold
        matches = get_close_matches(word, CITY_LIST, n=1, cutoff=0.75)
        return matches[0] if matches else None

    def _extract_dates(self, text: str):
        # Use dateparser to parse natural language dates
        # Try to find two dates in text or else fallback to regex dates
        dates = []

        # dateparser can find multiple dates with search_dates
        from dateparser.search import search_dates

        results = search_dates(text)
        if results:
            for _, dt in results:
                dates.append(dt.date())

        if len(dates) >= 2:
            dep = dates[0].strftime("%Y-%m-%d")
            ret = dates[1].strftime("%Y-%m-%d")
            return dep, ret
        elif len(dates) == 1:
            dep = dates[0].strftime("%Y-%m-%d")
            ret = (dates[0] + timedelta(days=self.default_trip_days)).strftime("%Y-%m-%d")
            return dep, ret

        # Fallback: regex for ISO date format
        matches = re.findall(r"'?(\d{4}-\d{2}-\d{2})'?", text)
        if len(matches) >= 2:
            return matches[0], matches[1]
        elif len(matches) == 1:
            dep = matches[0]
            ret = (datetime.strptime(dep, "%Y-%m-%d") + timedelta(days=self.default_trip_days)).strftime("%Y-%m-%d")
            return dep, ret

        return None, None

    def _extract_preference(self, text: str) -> str:
        # Semantic preference detection: check keyword presence with simple embedding-like similarity
        text_lower = text.lower()
        for keyword in self.preference_keywords:
            if keyword in text_lower:
                return keyword
        return self.default_preference


if __name__ == "__main__":
    parser = TravelQueryParser()
    print("\n🧳 Semantic Travel Query Parser (spaCy + fuzzy city + dateparser)\n")

    while True:
        query = input("🧭 Enter travel query (or type 'exit'): ")
        if query.lower() == "exit":
            break
        parsed = parser.parse(query)
        print("🎯 Parsed Info:", parsed)
