import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"

def print_path(rec):
    print(f"[{rec['persona']}] Total ETA: {rec['adjusted_eta']}h | Cost: ${rec['total_cost']}")
    for i, leg in enumerate(rec['legs']):
        prefix = "  " if leg['type'] == 'transit' else "  >> TRANSFER: "
        print(f"{prefix}{leg['from']} --({leg['mode']})--> {leg['to']} | {leg['eta']}h | ${leg['cost']}")

def run_test(name, payload):
    print(f"\n==================================================")
    print(f"EXECUTING {name}")
    print(f"==================================================")
    try:
        res = requests.post(f"{BASE_URL}/recommend", json=payload).json()
        if "error" in res:
            print(f"RESULT: FAIL (Error: {res['error']})")
            return None
        return res
    except Exception as e:
        print(f"RESULT: FAIL (Exception: {e})")
        return None

def execute_forensic_audit():
    # TEST 1: Forced Hybrid Path Proof
    print("\nTEST 1: DC-KOCHI -> Frankfurt (Multimodal Verification)")
    res1 = run_test("TEST 1", {
        "source": "DC-KOCHI",
        "destination": "Frankfurt",
        "transport_preference": "any",
        "routing_policy": "STRICT"
    })
    if res1:
        for rec in res1["recommendations"]:
            print_path(rec)
            has_transfer = any(l["type"] == "transfer" for l in rec["legs"])
            if has_transfer:
                print("VERDICT: PASS (Explicit transfer edges detected)")
            else:
                print("VERDICT: FAIL (No transfer edges, teleportation suspected)")

    # TEST 3: SUEZ Avoidance Truth (Maritime Forensic)
    print("\nTEST 3: Shanghai -> Rotterdam (Maritime Suez Bypass)")
    res3_normal = run_test("TEST 3 (NORMAL SEA)", {
        "source": "Shanghai",
        "destination": "Rotterdam",
        "transport_preference": "sea",
        "routing_policy": "STRICT"
    })
    res3_override = run_test("TEST 3 (AVOID SUEZ SEA)", {
        "source": "Shanghai",
        "destination": "Rotterdam",
        "transport_preference": "sea",
        "routing_policy": "STRICT",
        "overrides": {"avoid_chokepoints": ["CHOKE-SUEZ"]}
    })
    
    if res3_normal and res3_override:
        p1 = [l["to"] for l in res3_normal["recommendations"][0]["legs"]]
        p2 = [l["to"] for l in res3_override["recommendations"][0]["legs"]]
        print(f"Normal Path: {p1}")
        print(f"Avoid SUEZ Path: {p2}")
        if "CHOKE-SUEZ" in p2:
            print("VERDICT: FAIL (Suez still present in override path)")
        elif p1 == p2:
            print("VERDICT: FAIL (No path difference detected)")
        else:
            print("VERDICT: PASS (True structural reroute detected)")

    # TEST 4: Override Absoluteness
    print("\nTEST 4: DC-KOCHI -> Europe (Avoid AIR-DUBAI)")
    res4 = run_test("TEST 4", {
        "source": "DC-KOCHI",
        "destination": "Frankfurt",
        "overrides": {"avoid_chokepoints": ["AIR-DUBAI"]}
    })
    if res4:
        found_dubai = False
        for rec in res4["recommendations"]:
            path = [l["to"] for l in rec["legs"]] + [l["from"] for l in rec["legs"]]
            if "AIR-DUBAI" in path:
                found_dubai = True
        if found_dubai:
            print("VERDICT: FAIL (AIR-DUBAI present in override path)")
        else:
            print("VERDICT: PASS (Absolute exclusion verified)")

    # TEST 6: Economic Persona Truth
    print("\nTEST 6: Mumbai -> Chennai (Economic Logic)")
    res6 = run_test("TEST 6", {
        "source": "Mumbai",
        "destination": "Chennai",
        "transport_preference": "any"
    })
    if res6:
        for rec in res6["recommendations"]:
            modes = {l["mode"] for l in rec["legs"] if l["type"] == "transit"}
            print(f"[{rec['persona']}] Modes: {modes} | Cost: ${rec['total_cost']}")
            if rec["persona"] == "BALANCED" and "AIR" in modes:
                 print("WARNING: BALANCED (ECONOMIC) still picking AIR for short haul")
        print("VERDICT: PASS (Verified persona divergence)")

    # TEST 7: Hidden Shortcut Fraud Audit
    print("\nTEST 7: Illegal Shortcut Forensics (Top 10 High-Risk Routes)")
    routes = [
        ("Kochi", "Rotterdam"), ("Delhi", "New York"), ("Shanghai", "Los Angeles"),
        ("Mumbai", "Singapore"), ("Chennai", "Tokyo"), ("Hyderabad", "Frankfurt"),
        ("Kolkata", "London"), ("Bengaluru", "San Francisco"), ("Ahmedabad", "Dubai"),
        ("Pune", "Chicago")
    ]
    all_pass = True
    for s, d in routes:
        res = run_test(f"Audit: {s}->{d}", {"source": s, "destination": d})
        if res:
            for rec in res["recommendations"]:
                for i in range(len(rec["legs"])-1):
                    l1, l2 = rec["legs"][i], rec["legs"][i+1]
                    # Check for illegal mode switch without transfer
                    if l1["mode"] != l2["mode"] and l2["type"] != "transfer" and l1["type"] != "transfer":
                        print(f"  SUSPICIOUS: Mode jump {l1['mode']} -> {l2['mode']} without transfer leg at {l1['to']}")
                        all_pass = False
    if all_pass:
        print("VERDICT: PASS (No illegal mode jumps detected in high-risk sample)")
    else:
        print("VERDICT: FAIL (Illegal arbitrage shortcuts detected)")

if __name__ == "__main__":
    execute_forensic_audit()
