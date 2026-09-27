import sys
import os

# Ensure we can import from backend
sys.path.append(os.getcwd())

import numpy as np
import joblib

def test_geographic_intelligence():
    print("--- SUPPLYCHAINER V2: GEOGRAPHIC INTELLIGENCE AUDIT ---")
    
    try:
        from backend.engine.threat_intelligence import ThreatIntelligencePredictor
        predictor = ThreatIntelligencePredictor()
        
        # Verification Cases
        cases = [
            ("Seattle", "Miami", "road", "Last_Mile", 0.0),
            ("Kochi", "Delhi", "rail", "Global_Freight", 0.0),
            ("Mumbai", "Chennai", "sea", "Global_Freight", 0.8), # Disrupted Sea
            ("Suez Canal", "Singapore Port", "sea", "Global_Freight", 0.9), # High Risk Choke Point
        ]
        
        for origin, dest, mode, leg, nlp in cases:
            res = predictor.predict_worst_case_delay(
                origin=origin,
                destination=dest,
                transport_mode=mode,
                leg_type=leg,
                nlp_score=nlp
            )
            
            print(f"\nCASE: {origin} -> {dest} ({mode.upper()})")
            print(f"  NLP Threat Score: {nlp}")
            print(f"  Raw Prediction: {res['raw_model_prediction']}h")
            print(f"  Final Delay (Calibrated): {res['final_delay_presented']}h")
            print(f"  Friction Floor: {res['baseline_systemic_friction']}h")
            print(f"  Rationale: {res['calibration_reason']}")
            
            # Audit Pharma traces
            if "ABBVIE" in str(res).upper() or "PHARMA" in str(res).upper():
                print("  CRITICAL FAILURE: Pharma trace detected in output.")
            else:
                print("  VERIFIED: No Pharma proxy traces detected.")

    except Exception as e:
        print(f"AUDIT FAILED: {e}")

if __name__ == "__main__":
    test_geographic_intelligence()
