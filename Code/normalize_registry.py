import json
import os

def normalize_registry():
    hubs_path = "backend/data/canonical_hubs.json"
    with open(hubs_path, "r") as f:
        hubs = json.load(f)
    
    # Map common city names to their hubs
    # This is a manual mapping for critical hubs to ensure 100% demo success
    CITY_GROUPS = {
        "Kochi": {"sea": "PORT-KOCHI", "rail": "RAIL-KOCHI", "air": "AIR-COK", "road": "DC-KOCHI"},
        "Mumbai": {"sea": "PORT-MUMBAI", "rail": "RAIL-NHAVASHEVA", "air": "AIR-MUMBAI", "road": "HUB-MUMBAI"},
        "Delhi": {"air": "AIR-DELHI", "rail": "RAIL-DELHI", "road": "ICD-DELHI"},
        "Shanghai": {"sea": "PORT-SHANGHAI", "air": "AIR-SHANGHAI", "rail": "RAIL-SHANGHAI", "road": "HUB-SHANGHAI"},
        "Singapore": {"sea": "PORT-SINGAPORE", "air": "AIR-CHANGI", "road": "HUB-SINGAPORE"},
        "Dubai": {"sea": "PORT-JEBEL", "air": "AIR-DUBAI", "road": "HUB-DUBAI"},
        "Rotterdam": {"sea": "PORT-ROTTERDAM", "road": "HUB-ROTTERDAM", "rail": "RAIL-ROTTERDAM"},
        "Hamburg": {"sea": "PORT-HAMBURG", "rail": "RAIL-HAMBURG", "road": "HUB-HAMBURG"},
        "Los Angeles": {"sea": "PORT-LOSANGELES", "rail": "RAIL-LOSANGELES", "air": "AIR-LAX", "road": "HUB-LOSANGELES"},
        "New York": {"sea": "PORT-NEWYORK", "air": "AIR-JFK", "road": "HUB-NEWYORK", "rail": "RAIL-NEWYORK"}
    }
    
    # We need to ensure these IDs actually exist or are created.
    # For now, we will create the mapping.
    
    # Add 'parent_city' to all hubs
    for hub in hubs:
        hub["parent_city"] = None
        for city, mapping in CITY_GROUPS.items():
            if hub["id"] in mapping.values():
                hub["parent_city"] = city
                break
        
        if not hub["parent_city"]:
            # Heuristic for others
            hub["parent_city"] = hub["display_name"].split(" of ")[-1].split(" Port")[0].split(" Air")[0].split(" Rail")[0]

    with open(hubs_path, "w") as f:
        json.dump(hubs, f, indent=2)
        
    # Generate the location registry from the groups
    with open("backend/data/canonical_locations.json", "w") as f:
        json.dump(CITY_GROUPS, f, indent=2)
    
    print("Registry normalized with parent_city and location mapping.")

if __name__ == "__main__":
    normalize_registry()
