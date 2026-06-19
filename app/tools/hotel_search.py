from typing import List, Dict
import httpx

#TODO: Add the flight api url
HOTEL_API_URL = ""

async def search_hotels(city: str, hotel_company: str, beds: str, price: str, checkin_date: str) -> List[Dict]:
    params = {
        "city": city,
        "hotel_company": hotel_company,
        "beds": beds,
        "price": price,
        "checkin_date": checkin_date
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                HOTEL_API_URL,
                params=params
            )
            response.raise_for_status()
            data = response.json()

            hotels = []
            for hotel in data.get("results", []):
                hotels.append({
                    "city": hotel.get("city"),
                    "hotel_company": hotel.get("hotel_company"),
                    "beds": hotel.get("beds"),
                    "price": hotel.get("price"),
                    "checkin_date": hotel.get("checkin_date")
                })

            return hotels
        
    except httpx.HTTPError as e:
        print(f"Hotel API error: {e}")

        return []