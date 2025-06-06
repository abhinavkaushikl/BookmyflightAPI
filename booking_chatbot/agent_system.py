# booking_chatbot/agent_system.py

from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFaceHub
from langchain.agents.agent_types import AgentType

from bookingdummyapi.dummy_api import DummyBookingAPI
from bookingdummyapi.parser import TravelQueryParser

class TravelBookingAgent:
    def __init__(self, llm_model_name: str = "google/flan-t5-large"):
        """
        Initialize the TravelBookingAgent with a language model and tools.
        """
        # Load FLAN model from HuggingFaceHub or local (change as needed)
        self.llm = HuggingFaceHub(repo_id=llm_model_name, model_kwargs={"temperature":0.2, "max_length":512})
        
        # Initialize domain logic classes
        self.api = DummyBookingAPI()
        self.parser = TravelQueryParser()
        
        # Wrap booking functions as LangChain Tools
        self.tools = [
            Tool(
                name="Flight Booking",
                func=self.book_flight,
                description="Use this tool to book a flight given destination and dates."
            ),
            Tool(
                name="Hotel Booking",
                func=self.book_hotel,
                description="Use this tool to book a hotel given destination and dates."
            )
        ]

        # Initialize LangChain agent with zero-shot react description
        self.agent = initialize_agent(self.tools, self.llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    def book_flight(self, query: str) -> str:
        """
        Parse user query and book flight using DummyBookingAPI.
        """
        parsed = self.parser.parse(query)
        flight_info = self.api.book_flight(
            destination=parsed["destination"],
            departure_date=parsed["departure_date"],
            return_date=parsed["return_date"]
        )
        return (f"Flight booked with PNR: {flight_info['pnr']}, "
                f"from {flight_info['departure_date']} to {flight_info['return_date']} "
                f"to {flight_info['destination']}.")

    def book_hotel(self, query: str) -> str:
        """
        Parse user query and book hotel using DummyBookingAPI.
        """
        parsed = self.parser.parse(query)
        hotel_info = self.api.book_hotel(
            destination=parsed["destination"],
            checkin=parsed["departure_date"],
            checkout=parsed["return_date"],
            preference=parsed["preferences"]
        )
        return (f"Hotel booked with ID: {hotel_info['booking_id']}, "
                f"Hotel: {hotel_info['hotel_name']} located {hotel_info['location']}, "
                f"from {hotel_info['checkin']} to {hotel_info['checkout']}.")

    def run(self, input_text: str) -> str:
        """
        Runs the LangChain agent with the input text and returns response.
        """
        response = self.agent.run(input_text)
        return response


if __name__ == "__main__":
    # Simple CLI interface for testing
    agent = TravelBookingAgent()
    print("Welcome to the Travel Booking Agent!")
    while True:
        user_input = input("Enter your booking request (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        response = agent.run(user_input)
        print(f"Agent: {response}\n")
