import pandas as pd
import json
import os

def generate_calibration_profiles():
    print("--- GENERATING STATISTICALLY DEFENSIBLE CALIBRATION PROFILES ---")
    
    dataset_path = "Supplychainer_Geographic_Dataset.csv"
    if not os.path.exists(dataset_path):
        print(f"CRITICAL: Dataset missing at {dataset_path}")
        return
        
    df = pd.read_csv(dataset_path)
    
    modes = df['Transport_Mode'].unique()
    profiles = {}
    
    for mode in modes:
        mode_data = df[df['Transport_Mode'] == mode]['Delay_Hours']
        
        # Floor: p5 (represents unavoidable operational friction in 95% of cases)
        floor = round(float(mode_data.quantile(0.05)), 1)
        
        # Cap: p95 (represents the 95th percentile worst-case observed)
        # We apply an 'Operational Reality Bound' to prevent infinite tail explosion
        raw_p95 = float(mode_data.quantile(0.95))
        
        # Physics-Based Maximum Bounds (Plausible Disruption Limits)
        # Road: 4 days, Rail: 6 days, Air: 3 days, Sea: 15 days
        physics_limits = {
            "road": 96.0,
            "rail": 144.0,
            "air": 72.0,
            "sea": 360.0
        }
        
        cap = round(min(raw_p95, physics_limits.get(mode, 240.0)), 1)
        
        profiles[mode] = {
            "floor": floor,
            "cap": cap,
            "p5_observed": floor,
            "p95_observed": round(raw_p95, 1),
            "derivation": f"Derived from historical p5/p95 logistics percentile analysis on geographic node corpora."
        }
        
    output_path = "Execution/calibration_profiles.json"
    if not os.path.exists('Execution'):
        os.makedirs('Execution')
        
    with open(output_path, 'w') as f:
        json.dump(profiles, f, indent=4)
        
    print(f"SUCCESS: Calibration profiles saved to {output_path}")
    for mode, p in profiles.items():
        print(f"  {mode.upper()}: Floor={p['floor']}h, Cap={p['cap']}h")

if __name__ == "__main__":
    generate_calibration_profiles()
