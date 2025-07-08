import requests, json
from db.save_to_db import save_outlets_to_db

# Load stores from McD API
def fetch_all_outlets():
    url = "https://www.mcdonalds.com.my/storefinder/index.php"
    payload = {
        "ajax": 1,
        "action": "get_nearby_stores",
        "distance": 100000,  # Large range to include all
        "lat": 3.1390,
        "lng": 101.6869,
        "state": "",
        "products": "",
        "address": "",
        "issuggestion": 0,
        "islocateus": 0
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)
    response.encoding = "utf-8-sig"
    data = json.loads(response.text)
    return data.get("stores", [])


if __name__ == "__main__":
    print("📦 Fetching data from McDonald's Malaysia API...")
    outlets = fetch_all_outlets()
    print(f"✅ Found {len(outlets)} outlets.")
    save_outlets_to_db(outlets)
