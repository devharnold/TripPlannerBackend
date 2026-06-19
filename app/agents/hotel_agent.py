import json
from datetime import datetime
from typing import Dict, Any

from pydantic import BaseModel, ValidationError
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.tools.bnb_search import search_hotels
from app.models import HotelSearchSchema

#Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="",
    temparature=0.2
)

SYSTEM_PROMPT = """
You are an Hotel Search Agent

Your responsibilities
- Extract Hotel search details
- Validate user travel requests
- Search for available rooms
- Recommend the best available option

Rules:
- Return only valid JSON
- Use YYYY-MM-DD for dates
- Dont include markdown
"""

# Airbnb Agent
class HotelAgent:
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
        
        hotels = await search_hotels(
            city=extracted_data["city"],
            hotel_company=extracted_data["hotel_company"],
            beds=extracted_data["beds"],
            price=extracted_data["price"],
            checkin_date=extracted_data["checkin_date"]
        )
        if not hotels:
            return {
                "status": "No hotels found for that date",
                "message": {
                    f"No hotel rooms found from "
                    f"{extracted_data['datetime']}"
                    f"{extracted_data['city']}"
                }
            }
        sorted_hotels = sorted(hotels, key=lambda x: x.get("location", "company", "price", float("inf")))
        cheapest_hotel = sorted_hotels[0]

        return {
            "status": "Success",
            "search_parameters": extracted_data,
            "recommend_hotel_option": cheapest_hotel,
            "all_hotels": sorted_hotels
        }
    
    async def extract_trip_details(self, user_prompt: str) -> Dict[str, Any]:
        # Use gemini to extract the details
        prompt = f"""
        Extract hotel search information from the user request.
        
        Return only valid JSON.
        Required JSON format:
        {{
            "location": "city",
            "accommodation": "beds",
            "charges": "price",
            "checkin_date": "YYYY-MM-DD"
        }}
        User request:
        {user_prompt}
        """
        try:
            response = await llm.invoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=user_prompt)
            ])
            raw_text = response.content.strip()

            # remove anything to do with markdown
            raw_text = raw_text.replace("```json", "")
            raw_text = raw_text.replace("```", "")

            parsed_data = json.loads(raw_text)

            validated_data = HotelSearchSchema(**parsed_data)

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
                "message": f"Hotel agent error: {str(e)}"
            }
        

    def validate_inputs(self, data: Dict[str, Any]) -> str | None:
        # validates extracted bnb data
        required_fields = ["location", "accommodation", "charges", "checkin_date"]

        for field in required_fields:
            if not data.get(field):
                return f"Missing field: {field}"
            
        try:
            datetime.strptime(data["checkin_date"], "%Y-%m-%d")

        except ValueError:
            return (
                "Invalid checkin date format. "
                "Use YYYY-MM-DD."
            )
        return None