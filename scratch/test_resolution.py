import os, sys
import networkx as nx
from typing import Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.engine.multimodal_network import create_multimodal_network
from backend.engine.threat_intelligence import ThreatIntelligencePredictor
from backend.engine.route_recommender import RouteRecommender

def test_node_resolution():
    network = create_multimodal_network()
    predictor = ThreatIntelligencePredictor()
    
    class SimulatorState:
        def __init__(self):
            self.weather_states = {}
    
    simulator = SimulatorState()
    recommender = RouteRecommender(network, predictor, simulator)
    
    print("--- TESTING MODE-AWARE NODE RESOLUTION ---")
    
    # Test 1: Port ID with Rail Mode (Kochi)
    print("\nScenario: PORT-KOCHI -> PORT-SHANGHAI with transport_mode='rail'")
    resolved_s = recommender.resolver.resolve_node("PORT-KOCHI", "rail")
    resolved_d = recommender.resolver.resolve_node("PORT-SHANGHAI", "rail")
    print(f"  Resolved: {resolved_s} -> {resolved_d}")
    
    if resolved_s == "RAIL-KOCHI" and resolved_d == "RAIL-SHANGHAI":
        print("✓ RESOLUTION VERIFIED: Correct mode-specific nodes found.")
    else:
        print(f"✗ RESOLUTION FAILED: Expected RAIL-KOCHI -> RAIL-SHANGHAI")

    # Test 2: Air ID with Sea Mode (Dubai)
    print("\nScenario: AIR-DUBAI -> AIR-SHANGHAI with transport_mode='sea'")
    resolved_s = recommender.resolver.resolve_node("AIR-DUBAI", "sea")
    resolved_d = recommender.resolver.resolve_node("AIR-SHANGHAI", "sea")
    print(f"  Resolved: {resolved_s} -> {resolved_d}")
    
    if resolved_s == "HUB-DUBAI" or resolved_s == "PORT-JEBEL":
        print("✓ RESOLUTION VERIFIED: Air ID translated to Sea-capable node.")
    else:
        print(f"✗ RESOLUTION FAILED: Expected HUB-DUBAI or PORT-JEBEL, got {resolved_s}")

if __name__ == "__main__":
    test_node_resolution()
