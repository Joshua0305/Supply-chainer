#!/usr/bin/env python3
"""Corridor Integrity Audit: Find orphan hubs, broken corridors, and ID mismatches."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load canonical hubs
with open("backend/data/canonical_hubs.json") as f:
    hubs = json.load(f)
hub_ids = {h["id"] for h in hubs}
hub_map = {h["id"]: h for h in hubs}

# Check which IDs the multimodal_network.py edges reference
edge_node_refs = set()
with open("backend/engine/multimodal_network.py") as f:
    src = f.read()

# Extract all quoted strings that look like hub IDs from edge definitions
import re
# Find all string literals in edge tuples
refs = re.findall(r'"([A-Z][A-Z0-9\-_ ]+)"', src)
for r in refs:
    if any(r.startswith(p) for p in ["AIR-","PORT-","RAIL-","CHOKE-","HUB-","INBOM","INMAA","INKCH","SGSIN","USLAX","USNYC","NLRTM","AEJEA","CNSHG"]):
        edge_node_refs.add(r)

print("=" * 70)
print("CORRIDOR INTEGRITY AUDIT")
print("=" * 70)

# 1. ID MISMATCH: Edge refs that don't exist in canonical registry
print("\n[1] EDGE REFERENCES vs CANONICAL REGISTRY")
old_ids_in_edges = edge_node_refs - hub_ids
print(f"  Edge node refs found in code: {len(edge_node_refs)}")
print(f"  Valid canonical IDs:          {len(edge_node_refs & hub_ids)}")
print(f"  BROKEN REFS (old IDs):        {len(old_ids_in_edges)}")
for oid in sorted(old_ids_in_edges):
    print(f"    ✗ {oid}")

# 2. ORPHAN ANALYSIS: Hubs with zero edges
connected = edge_node_refs & hub_ids
orphans = hub_ids - edge_node_refs
print(f"\n[2] ORPHAN ANALYSIS")
print(f"  Total canonical hubs:   {len(hub_ids)}")
print(f"  Connected to edges:     {len(connected)}")
print(f"  ORPHANS (no edges):     {len(orphans)} ({len(orphans)/len(hub_ids)*100:.1f}%)")

# Group orphans by type
orphan_by_type = {}
for oid in orphans:
    if oid in hub_map:
        t = hub_map[oid]["type"]
        orphan_by_type.setdefault(t, []).append(oid)
for t, ids in sorted(orphan_by_type.items()):
    print(f"    {t:20s}: {len(ids)} orphans")

# 3. CORRIDOR ANALYSIS
print(f"\n[3] CRITICAL CORRIDOR STATUS")
corridors = {
    "Asia→Europe (Sea)": ["PORT-SHANGHAI","PORT-SINGAPORE","PORT-MUMBAI","CHOKE-SUEZ","PORT-ROTTERDAM"],
    "India→ME→Europe": ["PORT-MUMBAI","PORT-JEBEL","CHOKE-SUEZ","PORT-ROTTERDAM"],
    "US→Europe (Sea)": ["PORT-NEWYORK","PORT-ROTTERDAM"],
    "China→CentralAsia→Europe (Rail)": ["RAIL-ZHENGZHOU","RAIL-KHORGOS","RAIL-MOSCOW","RAIL-WARSAW","RAIL-DUISBURG"],
    "Trans-Siberian": ["PORT-VLADIVOSTOK","RAIL-NOVOSIBIRSK","RAIL-EKATERINBURG","RAIL-MOSCOW"],
    "India Domestic Rail": ["PORT-KOCHI","PORT-MUMBAI","RAIL-DELHI","PORT-CHENNAI"],
    "US Intermodal": ["PORT-LOSANGELES","RAIL-LOSANGELES","RAIL-CHICAGO","PORT-NEWYORK"],
    "Africa→Europe": ["PORT-DURBAN","PORT-MOMBASA","CHOKE-SUEZ","PORT-ROTTERDAM"],
    "SE Asia→China": ["PORT-HOCHIMINH","PORT-SINGAPORE","PORT-SHANGHAI"],
    "LatAm→Asia": ["PORT-SANTOS","CHOKE-PANAMA","PORT-LOSANGELES","PORT-SHANGHAI"],
}

for name, nodes in corridors.items():
    present = [n for n in nodes if n in connected]
    missing = [n for n in nodes if n not in connected]
    orphaned = [n for n in nodes if n in orphans]
    status = "✓ CONNECTED" if len(missing) == 0 else f"✗ BROKEN ({len(missing)} gaps)"
    print(f"  {name:40s} {status}")
    if missing:
        for m in missing:
            label = hub_map[m]["display_name"] if m in hub_map else "NOT IN REGISTRY"
            print(f"      MISSING: {m} ({label})")

# 4. OLD ID → NEW ID MAPPING NEEDED
print(f"\n[4] OLD-TO-NEW ID MIGRATION TABLE")
old_to_new = {
    "CNSHG": "PORT-SHANGHAI",
    "SGSIN": "PORT-SINGAPORE", 
    "NLRTM": "PORT-ROTTERDAM",
    "INBOM": "PORT-MUMBAI",
    "INKCH": "PORT-KOCHI",
    "INMAA": "PORT-CHENNAI",
    "AEJEA": "PORT-JEBEL",
    "USNYC": "PORT-NEWYORK",
    "USLAX": "PORT-LOSANGELES",
    "AIR-PVG": "AIR-SHANGHAI",
    "AIR-DXB": "AIR-DUBAI",
    "AIR-FRA": "AIR-FRANKFURT",
    "AIR-ANC": "AIR-ANCHORAGE",
    "AIR-MEM": "AIR-MEMPHIS",
    "AIR-ORD": "AIR-CHICAGO",
    "AIR-DEL": "AIR-DELHI",
    "RAIL-CHI": "RAIL-CHICAGO",
    "RAIL-DUIS": "RAIL-DUISBURG",
    "HUB-DAL": "HUB-DALLAS",
    "RAIL- Zhengzhou": "RAIL-ZHENGZHOU",
}
for old, new in old_to_new.items():
    exists_old = old in hub_ids
    exists_new = new in hub_ids
    print(f"  {old:25s} → {new:25s}  old_exists={exists_old}  new_exists={exists_new}")

print(f"\n[5] VERDICT")
print(f"  The multimodal_network.py edge list uses OBSOLETE IDs.")
print(f"  {len(orphans)} of {len(hub_ids)} hubs ({len(orphans)/len(hub_ids)*100:.0f}%) are completely disconnected.")
print(f"  The graph MUST be rebuilt with canonical IDs and production corridors.")
