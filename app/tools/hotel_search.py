import httpx
from typing import List, Dict
from datetime import datetime
import os

#TODO: Add Hotel Provider API URL
HOTEL_API_URL=os.getenv("HOTEL_API_URL")

async def locate_hotel_rooms(city: str, hotel: str, prefered_checkin_date: datetime) -> List[Dict]:
    params = {
        "city": city,
        "hotel": hotel,
        "prefered_checkin_date": prefered_checkin_date
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                HOTEL_API_URL,
                params=params
            )
            response.raise_for_status()
            data = response.json()

            hotel_rooms = []
            for hotel in data.get("results", []):
                hotel_rooms.append({
                    "hotel_name": hotel.get("hotel_name"),
                    "hotel_location": hotel.get("hotel_location"),
                    "price_per_night": hotel.get("price_per_night"),
                    "amenities": hotel.get("amenities")
                })

            return hotel_rooms
        
    except httpx.HTTPError as e:
        print(f"Hotel Search API Error: {e}")

        return []