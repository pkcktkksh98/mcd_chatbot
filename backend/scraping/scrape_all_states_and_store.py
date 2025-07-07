from scraping.scrape_mcd import scrape_outlets_by_state
from db.save_to_db import save_outlets
from utils.geocode import geocode_and_get_hours
import time

# List of all Malaysian states
states = [
    "Kuala Lumpur", "Selangor", "Johor", "Pulau Pinang", "Perak", "Negeri Sembilan",
    "Melaka", "Kedah", "Kelantan", "Terengganu", "Pahang", "Perlis", "Sabah", "Sarawak", "Putrajaya", "Labuan"
]

all_outlets = []

for state in states:
    print(f"Scraping: {state}")
    outlets = scrape_outlets_by_state(state)

    for outlet in outlets:
        # Add state info
        outlet["state"] = state

        # Geocode if lat/lon not already present
        if "latitude" not in outlet or "longitude" not in outlet:
            lat = geocode_and_get_hours(outlet["latitude"])
            lon = geocode_and_get_hours(outlet["longitude"])
            outlet["latitude"] = lat
            outlet["longitude"] = lon
            time.sleep(1)  # Optional: avoid rate limit

    all_outlets.extend(outlets)

# Save all scraped data to DB
print(f"\nSaving {len(all_outlets)} outlets to DB...")
save_outlets(all_outlets)
print("✅ Done.")
