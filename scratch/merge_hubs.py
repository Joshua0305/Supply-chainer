import json

def merge_hubs():
    with open("backend/data/canonical_hubs.json", "r") as f:
        existing_hubs = json.load(f)
    
    with open("scratch/expanded_indian_hubs.json", "r") as f:
        new_hubs = json.load(f)
    
    hub_map = {h["id"]: h for h in existing_hubs}
    
    added_count = 0
    updated_count = 0
    
    for nh in new_hubs:
        if nh["id"] in hub_map:
            # Merge connections
            existing_conn = hub_map[nh["id"]].get("connections", [])
            existing_targets = {c["to"] for c in existing_conn}
            
            for c in nh["connections"]:
                if c["to"] not in existing_targets:
                    existing_conn.append(c)
                    existing_targets.add(c["to"])
            
            hub_map[nh["id"]]["connections"] = existing_conn
            updated_count += 1
        else:
            hub_map[nh["id"]] = nh
            added_count += 1
            
    final_hubs = list(hub_map.values())
    
    with open("backend/data/canonical_hubs.json", "w") as f:
        json.dump(final_hubs, f, indent=2)
    
    print(f"Merge Complete. Added: {added_count}, Updated: {updated_count}. Total Hubs: {len(final_hubs)}")

if __name__ == "__main__":
    merge_hubs()
