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

SYSTEM_PROMPT = """
You are an Airbnb Search Agent

Your responsibilities
- Extract Airbnb search details
- Validate user travel requests
- Search for available rooms
- Recommend the best available option

Rules:
- Return only valid JSON
- Use YYYY-MM-DD for dates
- Dont include markdown
"""

# Airbnb Agent
class AirbnbAgent:
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
        
        bnbs = await search_bnb(

        )
        if not bnbs:
            return {
                "status": "No bnbs found for that date",
                "message": {
                    f"No bnbs found from "
                    f"{extracted_data['datetime']}"
                    f"{extracted_data['city']}"
                }
            }
        sorted_bnbs = sorted(bnbs, key=lambda x: x.get("location", "price", float("inf")))
        cheapest_bnb = sorted_bnbs[0]

        return {
            "status": "Success",
            "search_parameters": extracted_data,
            "recommend_bnb_option": cheapest_bnb,
            "all_bnbs": sorted_bnbs
        }
    
    async def extract_trip_details(self, user_prompt: str) -> Dict[str, Any]:
        # Use gemini to extract the details
        prompt = f"""
        Extract bnb search information from the user request.
        
        Return only valid JSON.
        Required JSON format:
        {{
            "": "",
            "": "",
            "": "",
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

            # remove anything to do with markdown
            raw_text = raw_text.replace("```json", "")
            raw_text = raw_text.replace("```", "")

            parsed_data = json.loads(raw_text)

            validated_data = BnbSearchSchema(**parsed_data)
            return validated_data.model_dump()
        
        except json.JSONDecodeError:
            return {
                "status": "error",
                "message": "Failed to parse LLM response"
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
        
    def validate_inputs(self, data:Dict[str, Any]) -> str | None:
        required_fields = [""]

        for field in required_fields:
            if not data.get(field):
                return f"Missing field: {field}"
            
        try:
            datetime.strptime(data["checkin_date"], "%Y-%m-%d")

        except ValueError:
            return (
                "Invalid checkin date format"
                "USE YYYY-MM-DD."
            )
        
        return None
    