import requests
import os
from dotenv import load_dotenv

load_dotenv()
HERE_API_KEY = os.getenv("API_KEY")

def geocode_and_get_hours(place_name: str):
    url = "https://discover.search.hereapi.com/v1/discover"
    params = {
        "q": place_name,
        "at": "3.1390,101.6869",  # center of Kota Bharu, not KL
        "limit": 1,
        "apiKey": "i33RsjNa7OFXNpyhgj-QhYEE8U4MIN8Vn41NSKNS-xk"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # print("\n" + place_name)
        # print(f"{data}\n")

        if data["items"]:
            item = data["items"][0]
            position = item["position"]

            # Safely get opening hours
            hours_data = item.get("openingHours")
            if hours_data and isinstance(hours_data, list):
                hours = hours_data[0].get("text", ["Not available"])
            else:
                hours = ["Not available"]

            # print(f'Position: {position}')
            # print(f'Hours: {" | ".join(hours)}')

            return {
                "latitude": position["lat"],
                "longitude": position["lng"],
                "hours": " | ".join(hours)
            }
        else:
            return {"latitude": None, "longitude": None, "hours": "Not found"}

    except Exception as e:
        print(f"Error geocoding {place_name}: {e}")
        return {"latitude": None, "longitude": None, "hours": "Error"}

if __name__ == "__main__":
    place_name = "McDonald's Titiwangsa DT"
    result = geocode_and_get_hours(place_name)
    print(result)
