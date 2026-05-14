from app.agents.flight_agent import FlightAgent
from app.agents.hotel_agent import HotelAgent
from app.agents.activity_agent import ActivityAgent
from app.agents.budget_agent import BudgetAgent
from app.agents.planner_agent import PlannerAgent

from app.orchestrator.state_manager import WorkflowState


class TripWorkflow:

    def __init__(self):

        self.flight_agent = FlightAgent()
        self.hotel_agent = HotelAgent()
        self.activity_agent = ActivityAgent()
        self.budget_agent = BudgetAgent()
        self.planner_agent = PlannerAgent()

        self.state = WorkflowState()

    async def generate_trip(
        self,
        preferences: dict
    ):

        self.state.update_step("budgeting")

        budget_split = self.budget_agent.allocate_budget(
            preferences["budget"]
        )

        self.state.update_step("searching_flights")

        flights = await self.flight_agent.find_best_flights(
            origin=preferences["origin"],
            destination=preferences["destination"],
            departure_date=preferences["departure_date"]
        )

        self.state.update_step("searching_hotels")

        hotels = await self.hotel_agent.recommend_hotels(
            city=preferences["destination"],
            budget=budget_split["hotel"]
        )

        self.state.update_step("searching_activities")

        activities = await self.activity_agent.find_activities(
            city=preferences["destination"],
            interests=preferences["interests"]
        )

        self.state.update_step("building_itinerary")

        trip_plan = self.planner_agent.generate_itinerary(
            destination=preferences["destination"],
            flights=flights,
            hotels=hotels,
            activities=activities
        )

        self.state.update_step("completed")

        return {
            "trip": trip_plan,
            "workflow_state": self.state.get_state()
        }