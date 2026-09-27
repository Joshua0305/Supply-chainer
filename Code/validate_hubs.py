import json

with open("backend/data/canonical_hubs.json") as f:
    hubs = json.load(f)

ids = set()
dupes_id = []
aliases = {}
dupes_alias = []
missing = []
bad_modes = []
valid_modes = {"sea", "air", "road", "rail"}
types = {}
countries = {}

for h in hubs:
    if h["id"] in ids:
        dupes_id.append(h["id"])
    ids.add(h["id"])
    t = h["type"]
    types[t] = types.get(t, 0) + 1
    c = h["country"]
    countries[c] = countries.get(c, 0) + 1
    for a in h["aliases"]:
        al = a.lower()
        if al in aliases:
            dupes_alias.append(al)
        aliases[al] = h["id"]
    if not h.get("lat") or not h.get("lon"):
        missing.append(h["id"])
    for m in h["modes"]:
        if m not in valid_modes:
            bad_modes.append(h["id"])

print("Total:", len(hubs))
print("Dupe IDs:", len(dupes_id))
print("Dupe aliases:", len(dupes_alias))
print("Missing coords:", len(missing))
print("Bad modes:", len(bad_modes))
print("Types:", types)
print("Countries:", len(countries))
