import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.engine.multimodal_network import create_multimodal_network
from backend.engine.threat_intelligence import ThreatIntelligencePredictor
from backend.engine.simulator import LogisticsSimulator
from backend.engine.route_recommender import RouteRecommender
from backend.engine.weather_integration import APIWeatherProvider

def run_repro():
    print("Initializing Supplychainer Engine...")
    net = create_multimodal_network()
    predictor = ThreatIntelligencePredictor()
    simulator = LogisticsSimulator(net, weather_provider=APIWeatherProvider())
    demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    recommender = RouteRecommender(net, predictor, simulator, demo_mode=demo_mode)
    
    source = "AIR-COK"
    destination = "PORT-CHENNAI"
    mode = "road"
    policy = "STRICT"
    
    print(f"\n--- RUNNING REPRO: {source} -> {destination} ({mode}, {policy}) ---")
    result = recommender.recommend(
        source=source,
        destination=destination,
        transport_preference=mode,
        routing_policy=policy
    )
    
    if "error" in result:
        print(f"\nResult: ERROR - {result['error']}")
    else:
        print(f"\nResult: SUCCESS - Found {len(result['recommendations'])} routes")

if __name__ == "__main__":
    run_repro()
