import random

class DummyBookingAPI:
    def __init__(self):
        # defining PNR and HTL  prefixes
        self.flight_prefix = "PNR"
        self.hotel_prefix = "HTL"

    def book_flight(self, destination: str, departure_date: str, return_date: str) -> dict:
        return {
            "pnr": f"{self.flight_prefix}{random.randint(100000, 999999)}",
            "departure_date": departure_date,
            "return_date": return_date,
            "destination": destination
        }

    def book_hotel(self, destination: str, checkin: str, checkout: str, preference: str = "beach") -> dict:
        return {
            "booking_id": f"{self.hotel_prefix}{random.randint(100000, 999999)}",
            "hotel_name": "Sea Breeze Resort",
            "location": f"Near {preference.capitalize()}",
            "checkin": checkin,
            "checkout": checkout
        }