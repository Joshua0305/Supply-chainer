import json
import networkx as nx
import os, sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.engine.multimodal_network import create_multimodal_network, load_canonical_hubs

def run_audit():
    print("Starting Graph-Registry Integrity Audit...")
    
    # 1. Load Registry
    hubs = load_canonical_hubs()
    hub_ids = {h["id"] for h in hubs}
    hub_map = {h["id"]: h for h in hubs}
    
    # 2. Load Location Registry
    loc_path = "backend/data/canonical_locations.json"
    locations = {}
    if os.path.exists(loc_path):
        with open(loc_path, "r") as f:
            locations = json.load(f)
            
    # 3. Load Graph
    G = create_multimodal_network()
    graph_nodes = set(G.nodes())
    
    failures = []
    
    # Check Location Registry -> Hub Registry
    for city, entities in locations.items():
        for mode, hub_id in entities.items():
            if hub_id not in hub_ids:
                failures.append(f"LOCATION-HUB MISMATCH: City '{city}' mode '{mode}' resolves to '{hub_id}' but not in canonical_hubs.json")
            if hub_id not in graph_nodes:
                failures.append(f"LOCATION-GRAPH MISMATCH: City '{city}' mode '{mode}' resolves to '{hub_id}' but not in NetworkX graph")

    # Check Hub Registry -> Graph
    for hub in hubs:
        hid = hub["id"]
        if hid not in graph_nodes:
            failures.append(f"HUB-GRAPH MISMATCH: Hub '{hid}' in registry but not in NetworkX graph")
        else:
            # Check for edge connectivity
            edges = list(G.edges(hid))
            if not edges:
                failures.append(f"ORPHAN HUB: '{hid}' in graph but has ZERO edges")
            else:
                # Mode specific connectivity
                for mode in hub["modes"]:
                    mode_edges = [d for u,v,d in G.edges(hid, data=True) if d.get("transport_mode") == mode]
                    if not mode_edges and mode != "road": # Local auto-wiring might handle road later
                        failures.append(f"MODE DISCONNECT: Hub '{hid}' supports '{mode}' but has no edges for this mode")

    # Check for Specific Failures mentioned by user
    if "AIR-COK" not in graph_nodes:
        failures.append("SPECIFIC FAILURE: AIR-COK missing from graph")
    
    # Mumbai Road Path Test
    # Find Mumbai Road Node
    mumbai_road = None
    for city, ent in locations.items():
        if city == "Mumbai": mumbai_road = ent.get("road")
    
    kochi_road = None
    for city, ent in locations.items():
        if city == "Kochi": kochi_road = ent.get("road")
        
    if mumbai_road and kochi_road:
        if mumbai_road in graph_nodes and kochi_road in graph_nodes:
            try:
                path = nx.shortest_path(G, kochi_road, mumbai_road, weight="baseline_time")
                print(f"Audit: Path from {kochi_road} to {mumbai_road} exists: {path}")
            except:
                failures.append(f"CONNECTIVITY FAILURE: No path found from {kochi_road} to {mumbai_road} (Road)")
        else:
            failures.append(f"CONNECTIVITY TEST SKIPPED: Road nodes for Kochi/Mumbai missing from graph")

    # Report
    with open("GRAPH_REGISTRY_AUDIT.md", "w") as f:
        f.write("# GRAPH-REGISTRY INTEGRITY AUDIT REPORT\n")
        f.write(f"Total Canonical Hubs: {len(hubs)}\n")
        f.write(f"Total Graph Nodes: {len(graph_nodes)}\n")
        f.write(f"Total Failures: {len(failures)}\n\n")
        
        if not failures:
            f.write("## ✓ ALL TESTS PASSED. SYSTEM IN SYNC.\n")
        else:
            f.write("## ✗ FAILURES DETECTED\n")
            for fail in failures:
                f.write(f"- {fail}\n")
                
    print(f"Audit complete. {len(failures)} failures found. See GRAPH_REGISTRY_AUDIT.md")

if __name__ == "__main__":
    run_audit()
