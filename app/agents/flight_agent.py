import json
from datetime import datetime
from typing import Dict, Any

from pydantic import BaseModel, ValidationError
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.tools.flight_search import search_flights

#Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="",
    temparature=0.2
)

class FlightSearchSchema(BaseModel):
    origin: str
    destination: str
    depature_date: datetime

# System Prompt
SYSTEM_PROMPT = """
You are a flight search agent

Your responsibilities:
- Extract flight search details
- Validate user travel requests
- Search for flights
- Recommend the best available option

Rules:
- Return only valid JSON
- Use YYYY-MM-DD for dates
- Do not include markdown
"""

# Flight Agent
class FlightAgent:
    async def run(self, user_prompt: str) -> Dict[str, Any]:
        extracted_data = await self.extract_trip_details(user_prompt)

        if extracted_data.get("status") == "error":
            return extracted_data
        
        validation_error = self.validate_inputs(extracted_data)
        if validation_error:
            return {
                "status": "Missing Information",
                "message": validation_error
            }
        
        flights = await search_flights(
            origin=extracted_data["origin"],
            destination=extracted_data["destination"],
            depature_date=extracted_data["depature_date"]
        )
        if not flights:
            return {
                "status": "No flights found",
                "message": (
                    f"No flights found from "
                    f"{extracted_data['origin']} to "
                    f"{extracted_data['destination']}."
                )
            }
        
        sorted_flights = sorted(flights, key=lambda x: x.get("price", float("inf")))
        cheapest_flight = sorted_flights[0]

        return {
            "status": "Success",
            "search_parameters": extracted_data,
            "recommend_flight": cheapest_flight,
            "all_flights": sorted_flights
        }
    
    async def extract_trip_details(self, user_prompt: str) -> dict[str, Any]:
        # Use gemini to extract trip details
        prompt = f"""
        Extract flight search information from the user request.
        
        Return only valid JSON.
        Required JSON format:
        {{
            "origin": "City",
            "destination": "City",
            "depature_date": "YYYY-MM-DD"
        }}
        User request:
        {user_prompt}
        """
        try:
            response = await llm.ainvoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=user_prompt)
            ])
            raw_text = response.content.strip()

            # remove anything to do w markdown
            raw_text = raw_text.replace("```json", "")
            raw_text = raw_text.replace("```", "")

            parsed_data = json.loads(raw_text)

            validated_data = FlightSearchSchema(**parsed_data)

            return validated_data.model_dump()
        
        except json.JSONDecodeError:
            return {
                "status": "error",
                "message": "Failed to parse LLM response."
            }
        
        except ValidationError as e:
            return {
                "status": "error",
                "message": str(e)
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Flight agent error: {str(e)}"
            }
        
    def validate_inputs(self, data: Dict[str, Any]) -> str | None:
        # validates extracted flight data
        required_fiels = ["origin", "destination", "depature_date"]

        for field in required_fiels:
            if not data.get(field):
                return f"Missing field: {field}"
            
        try:
            datetime.strptime(data["depature_date"], "%Y-%m-%d")

        except ValueError:
            return (
                "Invalid depature date format. "
                "Use YYYY-MM-DD."
                )
        return None
