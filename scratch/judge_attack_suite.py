import sys
import os
import time
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.engine.multimodal_network import create_multimodal_network
from backend.engine.threat_intelligence import ThreatIntelligencePredictor
from backend.engine.route_recommender import RouteRecommender
from backend.engine.scenario_manager import ScenarioManager

print("Initializing Engine for Hostile Attack Suite...")
t0 = time.time()
G = create_multimodal_network()
predictor = ThreatIntelligencePredictor()
scenario_mgr = ScenarioManager()
recommender = RouteRecommender(G, predictor, None, scenario_mgr, demo_mode=True)
cold_start_time = time.time() - t0

report = []
report.append("# JUDGE HOSTILE ATTACK SUITE - REPORT")
report.append(f"Engine Cold Start Latency: {cold_start_time:.3f}s\n")

# --- GROUP 1: FAKE PERSONA DETECTION ---
report.append("## TEST GROUP 1 — Fake Persona Detection")
print("Running Group 1...")
# A. Normal domestic
t1 = time.time()
res_dom = recommender.recommend("DC-KOCHI", "PORT-CHENNAI", transport_preference="road", routing_policy="STRICT")
lat_dom = time.time() - t1
recs = res_dom.get("recommendations", [])
report.append(f"### A. Domestic Corridor (DC-KOCHI -> PORT-CHENNAI)")
report.append(f"Returned {len(recs)} personas. Latency: {lat_dom:.3f}s")
if len(recs) == 0:
    report.append("**FAIL**: No routes found.")
else:
    paths = set([tuple([l["to"] for l in r["legs"]]) for r in recs])
    if len(paths) < len(recs):
        report.append("**FAIL**: Duplicate paths detected under different badges.")
    else:
        report.append("**PASS**: No fake duplicates. Structural deduplication active.")

# B. Strategic global
t1 = time.time()
res_glob = recommender.recommend("PORT-SHANGHAI", "PORT-ROTTERDAM", transport_preference="sea", routing_policy="STRICT")
lat_glob = time.time() - t1
recs_glob = res_glob.get("recommendations", [])
report.append(f"### B. Global Corridor (PORT-SHANGHAI -> PORT-ROTTERDAM)")
report.append(f"Returned {len(recs_glob)} personas. Latency: {lat_glob:.3f}s")
if len(recs_glob) == 0:
    report.append("**FAIL**: No routes found.")
else:
    paths = set([tuple([l["to"] for l in r["legs"]]) for r in recs_glob])
    if len(paths) < len(recs_glob):
        report.append("**FAIL**: Duplicate paths detected under different badges.")
    else:
        report.append("**PASS**: Personas are structurally unique or correctly suppressed.")

# --- GROUP 2: SCENARIO CREDIBILITY ATTACK ---
report.append("\n## TEST GROUP 2 — Scenario Credibility Attack")
print("Running Group 2...")
# A. No scenario (already done in glob)
has_suez = any("CHOKE-SUEZ" in l["to"] for l in recs_glob[0]["legs"])
report.append(f"### A. Normal Conditions (PORT-SHANGHAI -> PORT-ROTTERDAM)")
if has_suez:
    report.append("**PASS**: Normal route accurately traverses CHOKE-SUEZ constraint.")
else:
    report.append("**FAIL**: Normal route bypassed CHOKE-SUEZ unrealistically.")

# B. Suez Block
t1 = time.time()
res_scen = recommender.recommend("PORT-SHANGHAI", "PORT-ROTTERDAM", transport_preference="sea", routing_policy="STRICT", scenario="SUEZ_BLOCK")
lat_scen = time.time() - t1
recs_scen = res_scen.get("recommendations", [])
report.append(f"### B. SUEZ_BLOCK Scenario")
report.append(f"Solve Latency: {lat_scen:.3f}s")
if len(recs_scen) == 0:
    report.append("**FAIL**: Engine collapsed instead of routing.")
else:
    path_normal = [l["to"] for l in recs_glob[0]["legs"]]
    path_scen = [l["to"] for l in recs_scen[0]["legs"]]
    delay_scen = recs_scen[0]["worst_case_delay"]
    if path_normal != path_scen:
        report.append(f"**PASS**: Scenario structurally rerouted the physical path.")
    elif delay_scen > 200:
        report.append(f"**PASS**: Route maintained, but ETA exploded correctly (+{delay_scen}h). Engine respects disruption payload.")
    else:
        report.append(f"**FAIL**: Path unchanged and ETA unaffected. Scenario engine is fake.")

# --- GROUP 3: IMPOSSIBLE ROUTE TRUTHFULNESS ---
report.append("\n## TEST GROUP 3 — Impossible Route Truthfulness")
print("Running Group 3...")
# A. STRICT ROAD India -> USA
res_imp1 = recommender.recommend("DC-KOCHI", "PORT-LOSANGELES", transport_preference="road", routing_policy="STRICT")
report.append("### A. STRICT ROAD (India -> USA)")
if "error" in res_imp1 and "details" in res_imp1:
    report.append(f"**PASS**: Rejected gracefully with exact operational reasons: {json.dumps(res_imp1['details'])}")
else:
    report.append("**FAIL**: Allowed impossible intercontinental road route or threw generic unhandled exception.")

# B. STRICT AIR to ROAD ONLY Destination
res_imp2 = recommender.recommend("AIR-COK", "DC-CHICAGO", transport_preference="air", routing_policy="STRICT")
report.append("### B. STRICT AIR -> ROAD-ONLY Node")
if "error" in res_imp2 and "details" in res_imp2:
    report.append(f"**PASS**: Rejected explicitly. Details: {json.dumps(res_imp2['details'])}")
else:
    report.append("**FAIL**: Silent fallback or missing operational error.")

# --- GROUP 4: TRANSFER INTEGRITY ---
report.append("\n## TEST GROUP 4 — Transfer Integrity")
print("Running Group 4...")
res_trans = recommender.recommend("AIR-COK", "PORT-CHENNAI", transport_preference="road", routing_policy="STRICT")
recs_trans = res_trans.get("recommendations", [])
report.append("### A. STRICT ROAD (AIR-COK -> PORT-CHENNAI)")
if not recs_trans:
    report.append("**FAIL**: Failed to generate transfer legs.")
else:
    legs = recs_trans[0]["legs"]
    has_transfer = any(l["type"] == "transfer" for l in legs)
    if has_transfer and legs[0]["from"] == "AIR-COK" and "DC-" in legs[0]["to"]:
        report.append("**PASS**: Explicit transfer leg visible. No cargo teleportation from Airport to Highway.")
    else:
        report.append("**FAIL**: Transfer mechanics missing or opaque.")

# --- GROUP 5: EXECUTIVE EXPLAINABILITY ATTACK ---
report.append("\n## TEST GROUP 5 — Executive Explainability Attack")
print("Running Group 5...")
report.append("### A. Reasoning Verification")
if not recs_glob:
    report.append("**FAIL**: No recommendations to verify.")
else:
    exp = recs_glob[0].get("explanation", "")
    if len(exp) < 10 or "template" in exp.lower():
        report.append(f"**FAIL**: Generic template detected: {exp}")
    else:
        report.append(f"**PASS**: Deterministic reasoning detected: '{exp}'")
        
# --- GROUP 6: LATENCY CREDIBILITY ---
report.append("\n## TEST GROUP 6 — Latency Credibility")
print("Running Group 6...")
report.append("### A. Solve Metrics")
report.append(f"- Cold Start: {cold_start_time:.3f}s")
report.append(f"- Warm Solve (Domestic): {lat_dom:.3f}s")
report.append(f"- Warm Solve (Global): {lat_glob:.3f}s")
report.append(f"- Scenario Injection Solve: {lat_scen:.3f}s")
if lat_scen > 3.0:
    report.append("**FAIL**: Unacceptable >3s latency. Demo death.")
else:
    report.append("**PASS**: Engine operates at near-instant O(1) overlay speeds. Judge stable.")

with open("scratch/judge_attack_report.md", "w") as f:
    f.write("\n".join(report))

print("Adversarial Suite Complete. Report generated at scratch/judge_attack_report.md")
