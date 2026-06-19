import asyncio

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

    async def generate_trip(self, preferences: dict):
        state = WorkflowState()
        try:
            state.update_step("budgeting")
            budget_split = self.budget_agent.allocate_budget(
                preferences["budget"]
            )

            state.update_step("parallel_search")

            flights_task = self.flight_agent.find_best_flights(
                origin=preferences["origin"],
                destination=preferences["destination"],
                departure_date=preferences["departure_date"]
            )

            hotels_task = self.hotel_agent.recommend_hotels(
                city=preferences["destination"],
                budget=budget_split["hotel"]
            )

            activities_task = self.activity_agent.find_activities(
                city=preferences["destination"],
                interests=preferences["interests"]
            )

            flights, hotels, activities = await asyncio.gather(
                flights_task,
                hotels_task,
                activities_task
            )
            state.update_step("building_itinerary")

            trip_plan = await self.planner_agent.generate_itinerary(
                destination=preferences["destination"],
                flights=flights,
                hotels=hotels,
                activities=activities,
                budget=preferences["budget"]
            )
            state.update_step("completed")

            return {
                "status": "success",
                "trip": trip_plan,
                "workflow_state": state.get_state()
            }

        except Exception as e:
            state.add_error(str(e))
            return {
                "status": "error",
                "message": str(e),
                "workflow_state": state.get_state()
            }