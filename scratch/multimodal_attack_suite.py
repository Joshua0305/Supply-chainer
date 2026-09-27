import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_multimodal_integrity():
    print("--- PHASE 2: MULTIMODAL INTEGRITY ATTACK SUITE ---")
    
    # 1. Kochi -> Rotterdam (Should produce a Sea/Road/Rail hybrid)
    print("\nTEST 1: Kochi -> Rotterdam (Long Haul Multimodal)")
    payload = {
        "source": "Kochi",
        "destination": "Rotterdam",
        "transport_preference": "any",
        "routing_policy": "STRICT",
        "cargo_type": "general",
        "priority": "normal"
    }
    res = requests.post(f"{BASE_URL}/recommend", json=payload).json()
    if "error" in res:
        print(f"FAILED: {res['error']}")
    else:
        for rec in res["recommendations"]:
            modes = [leg["mode"] for leg in rec["legs"]]
            print(f"[{rec['persona']}] Path: {' -> '.join(modes)}")
            print(f"  ETA: {rec['adjusted_eta']}h | Cost: ${rec['total_cost']}")

    # 2. Avoid SUEZ (Should force Cape of Good Hope or Air shift)
    print("\nTEST 2: Avoid SUEZ (Strategic Reroute)")
    payload["overrides"] = {"avoid_chokepoints": ["CHOKE-SUEZ"]}
    res = requests.post(f"{BASE_URL}/recommend", json=payload).json()
    if "error" in res:
        print(f"FAILED: {res['error']}")
    else:
        for rec in res["recommendations"]:
             print(f"[{rec['persona']}] Override Applied: {rec['override_applied']}")
             print(f"  ETA composed: {rec['audit_trace']['eta']}")

    # 3. India -> USA STRICT ROAD (Must fail honestly)
    print("\nTEST 3: India -> New York (STRICT ROAD - Impossible)")
    payload = {
        "source": "Delhi",
        "destination": "New York",
        "transport_preference": "road",
        "routing_policy": "STRICT"
    }
    res = requests.post(f"{BASE_URL}/recommend", json=payload).json()
    if "error" in res:
        print(f"SUCCESS: Correctly failed with: {res['error']}")
    else:
        print(f"FAILURE: Faked a road path to USA!")

if __name__ == "__main__":
    test_multimodal_integrity()
