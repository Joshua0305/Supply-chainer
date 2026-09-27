import json
from typing import Dict, List, Any, Optional

class ScenarioManager:
    """
    Supplychainer Scenario Trigger Engine.
    Injects deterministic disruptions for judge-facing demonstrations.
    """
    SCENARIOS = {
        "SUEZ_BLOCK": {
            "name": "Suez Canal Blockage",
            "description": "Critical maritime corridor obstructed by vessel grounding.",
            "affected_nodes": ["CHOKE-SUEZ"],
            "threat_level": 1.0,
            "delay_hours": 240, # 10 days
            "reason": "Vessel grounding in Canal Narrows. Canal authority estimates 10-day salvage window.",
            "mode": "sea"
        },
        "RED_SEA_CONFLICT": {
            "name": "Red Sea Escalation",
            "description": "Increased regional instability affecting Bab el-Mandeb.",
            "affected_nodes": ["CHOKE-BABEL"],
            "threat_level": 0.85,
            "delay_hours": 72,
            "reason": "Regional conflict escalation. Vessels rerouting via Cape of Good Hope for risk mitigation.",
            "mode": "sea"
        },
        "LA_PORT_STRIKE": {
            "name": "LA Port Strike",
            "description": "Labor dispute causing terminal shutdowns in Los Angeles.",
            "affected_nodes": ["PORT-LOSANGELES", "PORT-LONGBEACH"],
            "threat_level": 0.9,
            "delay_hours": 120,
            "reason": "Terminal labor strike. Picket lines at all major berths. Throughput at 0%.",
            "mode": "sea"
        },
        "CHENNAI_FLOOD": {
            "name": "Chennai Monsoon Flooding",
            "description": "Extreme weather disrupting South India logistics.",
            "affected_nodes": ["PORT-CHENNAI", "HUB-CHENNAI"],
            "threat_level": 0.75,
            "delay_hours": 48,
            "reason": "Severe urban flooding. Inland road access to Port and Logistics Park is underwater.",
            "mode": "road"
        },
        "DUBAI_AIR_CONGESTION": {
            "name": "Dubai Hub Surge",
            "description": "Massive cargo backlog at DXB/DWC.",
            "affected_nodes": ["AIR-DUBAI"],
            "threat_level": 0.65,
            "delay_hours": 24,
            "reason": "Regional cargo surge exceeding ground handling capacity. 48h clearance backlog.",
            "mode": "air"
        },
        "HORMUZ_CLOSURE": {
            "name": "Hormuz Strait Escalation",
            "description": "Strategic maritime choke point tension.",
            "affected_nodes": ["CHOKE-HORMUZ"],
            "threat_level": 1.0,
            "delay_hours": 168,
            "reason": "Strategic naval activity. Vessels holding position at Jebel Ali / Colombo.",
            "mode": "sea"
        }
    }

    def __init__(self):
        self.active_scenario_id = None

    def activate_scenario(self, scenario_id: Optional[str]):
        if scenario_id and scenario_id in self.SCENARIOS:
            self.active_scenario_id = scenario_id
            return self.SCENARIOS[scenario_id]
        self.active_scenario_id = None
        return None

    def get_active_disruptions(self) -> Dict[str, Any]:
        if not self.active_scenario_id:
            return {}
        
        scenario = self.SCENARIOS[self.active_scenario_id]
        disruptions = {}
        for node in scenario["affected_nodes"]:
            disruptions[node] = {
                "delay": scenario["delay_hours"],
                "threat": scenario["threat_level"],
                "reason": scenario["reason"],
                "source": "SCENARIO_OVERRIDE"
            }
        return disruptions

    def get_all_scenarios(self) -> List[Dict[str, Any]]:
        return [{"id": k, **v} for k, v in self.SCENARIOS.items()]
