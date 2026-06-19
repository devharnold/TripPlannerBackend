from typing import List, Dict
import httpx
import os

#TODO: Add the flight api url
FLIGHT_API_URL = os.getenv("FLIGHT_API_URL")

async def search_flights(origin: str, destination: str, departure_date: str) -> List[Dict]:
    params = {
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                FLIGHT_API_URL,
                params=params
            )
            response.raise_for_status()
            data = response.json()

            flights = []
            for flight in data.get("results", []):
                flights.append({
                    "airline": flight.get("airline"),
                    "departure_time": flight.get("departure_time"),
                    "arrival_time": flight.get("arrival_time"),
                    "price": flight.get("price"),
                    "currency": flight.get("currency"),
                    "duration": flight.get("duration")
                })

            return flights
        
    except httpx.HTTPError as e:
        print(f"Flight API error: {e}")

        return []