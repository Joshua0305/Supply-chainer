import json
import os

MISSING_HUBS = [
    {"id": "ICD-DELHI", "display_name": "Inland Container Depot Delhi", "aliases": ["Tughlakabad", "Delhi ICD"], "type": "rail_hub", "modes": ["rail", "road"], "lat": 28.5000, "lon": 77.2800, "country": "India", "importance": 8, "strategic_role": "India's largest dry port"},
    {"id": "HUB-SINGAPORE", "display_name": "Singapore Logistics Center", "aliases": ["Tuas Hub"], "type": "distribution_hub", "modes": ["road"], "lat": 1.3521, "lon": 103.8198, "country": "Singapore", "importance": 9, "strategic_role": "Global transshipment distribution anchor"},
    {"id": "RAIL-ROTTERDAM", "display_name": "Rotterdam Intermodal Rail", "aliases": ["Maasvlakte Rail"], "type": "rail_hub", "modes": ["rail", "road"], "lat": 51.9225, "lon": 4.4792, "country": "Netherlands", "importance": 9, "strategic_role": "Europe's primary port-rail gateway"},
    {"id": "HUB-HAMBURG", "display_name": "Hamburg Logistics Hub", "aliases": ["Hamburg DC"], "type": "distribution_hub", "modes": ["road"], "lat": 53.5511, "lon": 9.9937, "country": "Germany", "importance": 8, "strategic_role": "Northern Europe distribution anchor"},
    {"id": "HUB-LOSANGELES", "display_name": "LA Logistics Cluster", "aliases": ["Inland Empire DC"], "type": "distribution_hub", "modes": ["road"], "lat": 34.0522, "lon": -118.2437, "country": "USA", "importance": 9, "strategic_role": "US West Coast logistics anchor"},
    {"id": "HUB-NEWYORK", "display_name": "New York Logistics Center", "aliases": ["Newark Hub"], "type": "distribution_hub", "modes": ["road"], "lat": 40.7128, "lon": -74.0060, "country": "USA", "importance": 9, "strategic_role": "US East Coast distribution anchor"},
    {"id": "RAIL-NEWYORK", "display_name": "New York Rail Freight", "aliases": ["Jersey City Rail"], "type": "rail_hub", "modes": ["rail", "road"], "lat": 40.7128, "lon": -74.0060, "country": "USA", "importance": 8, "strategic_role": "Northeast US rail anchor"},
]

def add_missing_hubs():
    hubs_path = "backend/data/canonical_hubs.json"
    with open(hubs_path, "r") as f:
        hubs = json.load(f)
    
    ids = {h["id"] for h in hubs}
    added = 0
    for h in MISSING_HUBS:
        if h["id"] not in ids:
            h["connections"] = [] # Will be populated by connectivity generator
            hubs.append(h)
            added += 1
            
    with open(hubs_path, "w") as f:
        json.dump(hubs, f, indent=2)
    print(f"Added {added} missing strategic hubs to satisfy location registry.")

if __name__ == "__main__":
    add_missing_hubs()
