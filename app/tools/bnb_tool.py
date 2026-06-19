import httpx
from typing import List, Dict
from datetime import datetime
import os

#TODO: Add Hotel Provider API URL
AIR_BNB_URL=os.getenv("HOTEL_API_URL")

async def search_bnbs(location: str, beds: int, checkin_date: datetime) -> List[Dict]:
    params = {
        "location": location,
        "beds": beds,
        "checkin_date": checkin_date
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                AIR_BNB_URL,
                params=params
            )
            response.raise_for_status()
            data = response.json()

            available_options = []
            for bnb in data.get("results", []):
                available_options.append({
                    "location": bnb.get("location"),
                    "beds": bnb.get("beds"),
                    "checkin_date": bnb.get("checkin_date")
                })

            return available_options
        
    except httpx.HTTPError as e:
        print(f"Hotel Search API Error: {e}")

        return []