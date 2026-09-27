import sys
import os
import time
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.engine.multimodal_network import create_multimodal_network
from backend.engine.threat_intelligence import ThreatIntelligencePredictor
from backend.engine.route_recommender import RouteRecommender
from backend.engine.scenario_manager import ScenarioManager

print("\n--- MEASURING FAST BOOT ---")
t0 = time.time()
G = create_multimodal_network()
predictor = ThreatIntelligencePredictor(lazy_load=True)
scenario_mgr = ScenarioManager()
recommender = RouteRecommender(G, predictor, None, scenario_mgr, demo_mode=False)
fast_boot_latency = time.time() - t0
print(f"Fast Boot Latency: {fast_boot_latency:.3f}s")

print("\n--- MEASURING FIRST-REQUEST LATENCY (NON-BLOCKING) ---")
t1 = time.time()
res_cold = recommender.recommend("DC-KOCHI", "PORT-CHENNAI", transport_preference="road", routing_policy="STRICT")
first_request_latency = time.time() - t1
print(f"First Request Latency (Warming State): {first_request_latency:.3f}s")
assert recommender.is_warmed_up == False, "Engine should NOT be warmed up yet."
assert "recommendations" in res_cold, "Engine failed to resolve cold request."

print("\n--- TRIGGERING BACKGROUND WARMUP ---")
recommender.run_background_warmup()
assert recommender.is_warmed_up == True, "Engine should be warmed up now."

print("\n--- MEASURING DEMO_MODE FAST BOOT ---")
t0_demo = time.time()
recommender_demo = RouteRecommender(G, predictor, None, scenario_mgr, demo_mode=True)
demo_boot_latency = time.time() - t0_demo
print(f"DEMO_MODE Boot Latency: {demo_boot_latency:.3f}s")
assert recommender_demo.is_warmed_up == True, "DEMO_MODE must instantly skip warmup."

print("\n--- WARM-UP FAILURE HANDLING TEST ---")
predictor_fail = ThreatIntelligencePredictor(lazy_load=True)
# Break the NLP engine model path intentionally
recommender_fail = RouteRecommender(G, predictor_fail, None, scenario_mgr, demo_mode=False)
recommender_fail.nlp._ready = False # Mock NLP not ready
def fake_warmup(): raise Exception("Simulated ML Loading Out Of Memory Error")
recommender_fail.predictor.warmup = fake_warmup
recommender_fail.run_background_warmup()
assert recommender_fail.warmup_failed == True, "Failure not properly captured."

