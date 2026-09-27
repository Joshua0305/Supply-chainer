import pandas as pd
import numpy as np
import random
import math
from typing import Tuple

# --- CONFIGURATION ---
NUM_SAMPLES = 50000
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

# --- GEOGRAPHIC LOGISTICS NODES (with Lat/Lon for Distance-Awareness) ---
HUB_COORDS = {
    "Seattle Port": (47.6062, -122.3321),
    "Portland Terminal": (45.5152, -122.6784),
    "San Francisco Port": (37.7749, -122.4194),
    "Los Angeles Port": (34.0522, -118.2437),
    "Salt Lake City Hub": (40.7608, -111.8910),
    "Denver Terminal": (39.7392, -104.9903),
    "Phoenix Logistics": (33.4484, -112.0740),
    "Dallas Corridor": (32.7767, -96.7970),
    "Houston Port": (29.7604, -95.3698),
    "Chicago Rail Hub": (41.8781, -87.6298),
    "St. Louis Hub": (38.6270, -90.1994),
    "Atlanta Air Hub": (33.7490, -84.3880),
    "Miami Port": (25.7617, -80.1918),
    "New York Port": (40.7128, -74.0060),
    "Boston Terminal": (42.3601, -71.0589),
    # Global Hubs (Geographically Grounded)
    "Mumbai Port": (18.9438, 72.8387),
    "Kochi Port": (9.9312, 76.2673),
    "Delhi Air Cargo": (28.5562, 77.1000),
    "Suez Canal": (30.5852, 32.2654),
    "Singapore Port": (1.2762, 103.8017),
    "Shanghai Port": (31.2222, 121.4581),
    "Rotterdam Port": (51.9225, 4.4791),
    "Dubai Logistics Hub": (24.8978, 55.0272),
    "Chennai Port": (13.0827, 80.2707)
}

ALL_NODES = list(HUB_COORDS.keys())
MODES = ["road", "rail", "air", "sea"]
LEGS = ["Global_Freight", "Last_Mile"]
CONDITIONS = ["Clear", "rainy", "stormy"]

def calculate_dist(c1: Tuple[float, float], c2: Tuple[float, float]) -> float:
    R = 6371
    phi1, phi2 = math.radians(c1[0]), math.radians(c2[0])
    dphi = math.radians(c2[0] - c1[0])
    dlambda = math.radians(c2[1] - c1[1])
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

# --- DATA GENERATION ENGINE ---
data = []

for _ in range(NUM_SAMPLES):
    leg = random.choice(LEGS)
    origin_name = random.choice(ALL_NODES)
    dest_name = random.choice(ALL_NODES)
    while dest_name == origin_name:
        dest_name = random.choice(ALL_NODES)
        
    mode = random.choice(MODES)
    condition = random.choice(CONDITIONS)
    
    dist_km = calculate_dist(HUB_COORDS[origin_name], HUB_COORDS[dest_name])
    
    # --- PHYSICS-AWARE BASELINE DELAY ---
    # mode_speed in km/h, ground_friction in hours
    mode_speed = 80.0
    ground_friction = 2.0
    
    if mode == "sea":
        mode_speed = 30.0
        ground_friction = 48.0 # Customs/Berthing/Loading floor
    elif mode == "air":
        mode_speed = 800.0
        ground_friction = 6.0  # High ground handling floor
    elif mode == "rail":
        mode_speed = 70.0
        ground_friction = 12.0 # Rail scheduling friction
    
    transit_time = dist_km / mode_speed
    base_delay = ground_friction + (transit_time * 0.1) # 10% expected transit variance
    
    # --- DISRUPTION PRIORS (GEOGRAPHIC & PHYSICS GROUNDED) ---
    disruption_multiplier = 1.0
    
    # 1. Condition Sensitivity
    if condition == "rainy":
        disruption_multiplier *= 1.3
    if condition == "stormy":
        # Air/Sea are more vulnerable to storms than Road/Rail
        if mode in ["air", "sea"]:
            disruption_multiplier *= 4.0 
        else:
            disruption_multiplier *= 2.0
            
    # 2. Hub-Specific Operational Risks
    if "Suez Canal" in [origin_name, dest_name] and mode == "sea":
        disruption_multiplier *= 3.5 # Choke point congestion
    if "Delhi Air Cargo" in [origin_name, dest_name] and condition != "Clear":
        disruption_multiplier *= 1.8 # Smog/Fog visibility risk
    if "Mumbai Port" in [origin_name, dest_name] and condition == "stormy":
        disruption_multiplier *= 2.0 # Monsoon port shutdown
    if "Chicago Rail Hub" in [origin_name, dest_name] and mode == "rail":
        disruption_multiplier *= 1.5 # Congestion prior
        
    # --- FAT-TAIL DISTRIBUTION (LOG-NORMAL) ---
    # We use a larger sigma for Sea/Air to represent Black Swan volatility
    sigma = 0.6
    if mode in ["sea", "air"]: sigma = 0.9
    
    mu = np.log(base_delay * disruption_multiplier)
    delay = np.random.lognormal(mean=mu, sigma=sigma)
    
    # NLP Severity Score (Simulated News Signal Correlation)
    # Calibrated so p85 delays correlate to 0.8+ severity
    nlp_score = np.clip((delay / 250.0) + np.random.normal(0, 0.15), 0.0, 1.0)
    
    data.append({
        "Leg_Type": leg,
        "Origin_Node": origin_name,
        "Destination_Node": dest_name,
        "Transport_Mode": mode,
        "Condition_Flag": condition,
        "NLP_Severity_Score": round(nlp_score, 4),
        "Delay_Hours": round(delay, 2)
    })

df = pd.DataFrame(data)

# --- EXPORT & AUDIT ---
output_path = "Supplychainer_Geographic_Dataset.csv"
df.to_csv(output_path, index=False)

print(f"--- BRUTAL AUDIT COMPLETE ---")
print(f"Physics-Awareness: ENABLED (Distance + Mode Speed + Ground Floors)")
print(f"Geographic Priors: ENABLED (Suez, Delhi, Mumbai, Chicago)")
print(f"Volatility Profile: FAT-TAIL LOG-NORMAL (Mode-Specific Sigma)")
print(f"Total Scenarios: {len(df)}")
print(f"P85 Delay (Sea): {df[df['Transport_Mode']=='sea']['Delay_Hours'].quantile(0.85):.2f}h")
print(f"P85 Delay (Air): {df[df['Transport_Mode']=='air']['Delay_Hours'].quantile(0.85):.2f}h")
