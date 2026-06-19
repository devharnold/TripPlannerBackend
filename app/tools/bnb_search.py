from typing import List, Dict
import httpx

#TODO: Add the flight api url
AIR_BNB_API_URL = ""

async def search_bnbs(city: str, beds: str, price: str, checkin_date: str, stay_duration: str) -> List[Dict]:
    params = {
        "city": city,
        "beds": beds,
        "price": price,
        "checkin_date": checkin_date
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                AIR_BNB_API_URL,
                params=params
            )
            response.raise_for_status()
            data = response.json()

            bnbs = []
            for bnb in data.get("results", []):
                bnbs.append({
                    "city": bnb.get("location"),
                    "beds": bnb.get("beds"),
                    "price": bnb.get("price"),
                    "checkin_date": bnb.get("checkin_date"),
                })

            return bnbs
        
    except httpx.HTTPError as e:
        print(f"Bnb API error: {e}")

        return []