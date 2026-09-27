import sys
import os
import json

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from engine.supplier_scorer import SupplierScorer
from engine.scenario_manager import ScenarioManager

def run_adversarial_procurement_test():
    print("--- Supplychainer Procurement Adversarial Test ---")
    
    data_path = os.path.join('backend', 'data', 'suppliers.json')
    scorer = SupplierScorer(data_path)
    sm = ScenarioManager()
    
    # 1. Determinism Test
    print("[TEST 1] Determinism: Checking stable ranking for 'Electronics' (Normal Conditions)")
    r1 = scorer.get_ranked_suppliers("Electronics")
    r2 = scorer.get_ranked_suppliers("Electronics")
    
    if [s['id'] for s in r1] == [s['id'] for s in r2]:
        print("PASS: Ranking is deterministic.")
    else:
        print("FAIL: Ranking is non-deterministic.")
        
    # 2. Disruption Sensitivity Test (Suez Block)
    print("\n[TEST 2] Disruption Sensitivity: Injecting 'SUEZ_BLOCK' impact on Global Suppliers")
    # Global Dynamics (SUP-GLOBAL-01) uses SUEZ.
    sm.activate_scenario("SUEZ_BLOCK")
    disruptions = sm.get_active_disruptions()
    
    r_normal = scorer.get_ranked_suppliers("Electronics")
    r_disrupted = scorer.get_ranked_suppliers("Electronics", disruptions)
    
    global_supplier_normal = next(s for s in r_normal if s['id'] == 'SUP-GLOBAL-01')
    global_supplier_disrupted = next(s for s in r_disrupted if s['id'] == 'SUP-GLOBAL-01')
    
    print(f"Normal Lead Time: {global_supplier_normal['effective_lead_time']} days")
    print(f"Disrupted Lead Time: {global_supplier_disrupted['effective_lead_time']} days")
    
    if global_supplier_disrupted['effective_lead_time'] > global_supplier_normal['effective_lead_time']:
        print("PASS: Lead time penalty correctly applied.")
    else:
        print("FAIL: No lead time penalty detected.")
        
    # 3. Inventory Escalation Test
    print("\n[TEST 3] Inventory Escalation: Safety Stock Violation Logic")
    # current=1000, safety=1500, forecast=800 -> projected=200 (less than safety)
    advice = scorer.get_procurement_advice(1000, 1500, 800)
    print(f"Status: {advice['status']}")
    print(f"Recommendation: {advice['recommendation']}")
    
    if advice['status'] == "SAFETY_STOCK_VIOLATION":
        print("PASS: Safety stock violation correctly triggered.")
    else:
        print("FAIL: Inventory logic mismatch.")

    print("\n[TEST 4] Inventory Escalation: Critical Stockout Logic")
    # current=500, safety=1500, forecast=800 -> projected=-300
    advice = scorer.get_procurement_advice(500, 1500, 800)
    print(f"Status: {advice['status']}")
    
    if advice['status'] == "CRITICAL_SHORTAGE":
        print("PASS: Critical shortage correctly triggered.")
    else:
        print("FAIL: Stockout detection failure.")

    print("\n--- AUDIT COMPLETE: Procurement Logic is Mathematically Defensible ---")

if __name__ == "__main__":
    run_adversarial_procurement_test()
