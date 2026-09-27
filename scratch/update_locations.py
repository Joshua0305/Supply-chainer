import json

def update_locations():
    with open("backend/data/canonical_hubs.json", "r") as f:
        hubs = json.load(f)
    
    with open("backend/data/canonical_locations.json", "r") as f:
        locations = json.load(f)
    
    # Map city -> mode -> hub_id
    city_map = {}
    for h in hubs:
        city = h.get("parent_city")
        if not city: continue
        
        if city not in city_map:
            city_map[city] = {}
        
        for mode in h["modes"]:
            # Prioritize higher importance hubs for the same mode
            current_hub = city_map[city].get(mode)
            if not current_hub:
                city_map[city][mode] = h["id"]
            else:
                # Find current hub's importance
                curr_imp = 0
                for h2 in hubs:
                    if h2["id"] == current_hub:
                        curr_imp = h2.get("importance", 0)
                        break
                if h.get("importance", 0) > curr_imp:
                    city_map[city][mode] = h["id"]

    # Merge into existing locations
    for city, modes in city_map.items():
        if city not in locations:
            locations[city] = modes
        else:
            for mode, hub_id in modes.items():
                if mode not in locations[city]:
                    locations[city][mode] = hub_id

    with open("backend/data/canonical_locations.json", "w") as f:
        json.dump(locations, f, indent=2)
    
    print(f"Location Map Updated. Total Cities: {len(locations)}")

if __name__ == "__main__":
    update_locations()
