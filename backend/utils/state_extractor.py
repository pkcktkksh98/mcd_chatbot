import re

states = [
    "Perlis", "Kedah", "Pulau Pinang", "Perak", "Selangor", "Negeri Sembilan",
    "Melaka", "Johor", "Pahang", "Terengganu", "Kelantan", "Sabah", "Sarawak",
    "Kuala Lumpur", "Putrajaya", "Labuan"
]

def extract_state_from_address(address: str) -> str:
    for state in states:
        if state.lower() in address.lower():
            return state
    return "Unknown"
