import json
import os

def generate_location_registry():
    hubs_path = "backend/data/canonical_hubs.json"
    with open(hubs_path, "r") as f:
        hubs = json.load(f)
    
    # Heuristic: Find common city names in aliases or display names
    # A better way is to explicitly tag them, but let's see if we can derive it
    
    city_map = {} # {city_name: {mode: hub_id}}
    
    # Pre-defined major cities to ensure correctness
    MAJOR_CITIES = [
        "Shanghai", "Singapore", "Mumbai", "Kochi", "Dubai", "Rotterdam", "Hamburg",
        "Los Angeles", "Chicago", "New York", "London", "Hong Kong", "Tokyo", "Busan",
        "Shenzhen", "Ningbo", "Guangzhou", "Qingdao", "Tianjin", "Dalian", "Xiamen",
        "Chennai", "Delhi", "Bangalore", "Hyderabad", "Kolkata", "Colombo", "Karachi",
        "Jebel Ali", "Salalah", "Jeddah", "Alexandria", "Piraeus", "Valencia", "Algeciras",
        "Antwerp", "Felixstowe", "Le Havre", "Gdansk", "Genoa", "Trieste", "Klaipeda",
        "Savannah", "Houston", "Seattle", "Oakland", "Charleston", "Long Beach",
        "Vancouver", "Prince Rupert", "Montreal", "Halifax", "Santos", "Sao Paulo",
        "Buenos Aires", "Callao", "Cartagena", "Lazaro Cardenas", "Manzanillo",
        "Durban", "Cape Town", "Mombasa", "Dar es Salaam", "Lagos", "Tanger Med",
        "Sydney", "Melbourne", "Brisbane", "Auckland"
    ]
    
    for city in MAJOR_CITIES:
        city_map[city] = {}
        for hub in hubs:
            # Match if city is in display name or aliases
            if city.lower() in hub["display_name"].lower() or any(city.lower() == a.lower() for a in hub["aliases"]):
                for mode in hub["modes"]:
                    if mode not in city_map[city]:
                        city_map[city][mode] = hub["id"]
    
    # Filter out empty cities
    city_map = {k: v for k, v in city_map.items() if v}
    
    with open("backend/data/canonical_locations.json", "w") as f:
        json.dump(city_map, f, indent=2)
    
    print(f"Generated Location Registry: {len(city_map)} cities mapped.")

if __name__ == "__main__":
    generate_location_registry()
