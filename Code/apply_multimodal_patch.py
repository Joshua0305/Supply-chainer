import json
import os

PATCH_HUBS = [
    {"id": "RAIL-KOCHI", "display_name": "Kochi Rail Intermodal Terminal", "aliases": ["Kochi Rail"], "type": "rail_hub", "modes": ["rail", "road"], "lat": 9.9312, "lon": 76.2673, "country": "India", "importance": 7, "strategic_role": "Southern India rail gateway"},
    {"id": "AIR-COK", "display_name": "Cochin International Airport", "aliases": ["COK", "Kochi Airport"], "type": "airport", "modes": ["air", "road"], "lat": 10.1520, "lon": 76.3920, "country": "India", "importance": 7, "strategic_role": "Major air cargo hub for Kerala"},
    {"id": "DC-KOCHI", "display_name": "Kochi Logistics Distribution Center", "aliases": ["Kochi DC"], "type": "distribution_hub", "modes": ["road"], "lat": 9.9800, "lon": 76.3000, "country": "India", "importance": 6, "strategic_role": "Last-mile hub for Kochi area"},
    {"id": "RAIL-SHANGHAI", "display_name": "Shanghai Railway Freight Terminal", "aliases": ["Shanghai Rail"], "type": "rail_hub", "modes": ["rail", "road"], "lat": 31.2304, "lon": 121.4737, "country": "China", "importance": 8, "strategic_role": "Yangtze Delta rail anchor"},
    {"id": "HUB-SHANGHAI", "display_name": "Shanghai Global Distribution Center", "aliases": ["Shanghai DC"], "type": "distribution_hub", "modes": ["road"], "lat": 31.2000, "lon": 121.5000, "country": "China", "importance": 8, "strategic_role": "Primary China export staging area"},
]

def apply_patch():
    hubs_path = "backend/data/canonical_hubs.json"
    with open(hubs_path, "r") as f:
        hubs = json.load(f)
    
    existing_ids = {h["id"] for h in hubs}
    added = 0
    for hub in PATCH_HUBS:
        if hub["id"] not in existing_ids:
            hubs.append(hub)
            added += 1
            
    with open(hubs_path, "w") as f:
        json.dump(hubs, f, indent=2)
    
    print(f"Applied multimodal patch: {added} hubs added.")

if __name__ == "__main__":
    apply_patch()
