import json
import os

def migrate_to_single_source():
    hubs_path = "backend/data/canonical_hubs.json"
    with open(hubs_path, "r") as f:
        hubs = json.load(f)
    
    # Hub ID lookup for quick validation
    hub_ids = {h["id"] for h in hubs}
    
    # 1. Hardcoded Strategic Connections from multimodal_network.py (MIGRATION DATA)
    # Sea
    SEA = [("PORT-SHANGHAI","PORT-SINGAPORE"),("PORT-SINGAPORE","CHOKE-MALACCA"),("CHOKE-MALACCA","PORT-COLOMBO"),
           ("PORT-COLOMBO","PORT-MUMBAI"),("PORT-MUMBAI","PORT-JEBEL"),("PORT-JEBEL","CHOKE-SUEZ"),
           ("CHOKE-SUEZ","PORT-PIRAEUS"),("PORT-PIRAEUS","PORT-VALENCIA"),("PORT-VALENCIA","PORT-ALGECIRAS"),
           ("PORT-ALGECIRAS","PORT-ROTTERDAM"),("PORT-ROTTERDAM","PORT-HAMBURG"),("PORT-SHANGHAI","PORT-BUSAN"),
           ("PORT-BUSAN","PORT-LONG_BEACH"),("PORT-LONG_BEACH","CHOKE-PANAMA"),("CHOKE-PANAMA","PORT-SAVANNAH"),
           ("PORT-SAVANNAH","PORT-NEWYORK"),("PORT-NEWYORK","PORT-ROTTERDAM"),("PORT-SHANGHAI","PORT-NINGBO"),
           ("PORT-NINGBO","PORT-SINGAPORE"),("PORT-MUNDRA","PORT-JEBEL"),("PORT-MUMBAI","PORT-CHENNAI"),
           ("PORT-CHENNAI","PORT-SINGAPORE"),("PORT-KOCHI","PORT-MUMBAI"),("PORT-KOCHI","PORT-COLOMBO"),
           ("PORT-SINGAPORE","PORT-SYDNEY"),("PORT-SYDNEY","PORT-AUCKLAND")]
    
    # Air
    AIR = [("AIR-SHANGHAI","AIR-CHANGI"),("AIR-CHANGI","AIR-DUBAI"),("AIR-DUBAI","AIR-FRANKFURT"),
           ("AIR-FRANKFURT","AIR-HEATHROW"),("AIR-HEATHROW","AIR-JFK"),("AIR-JFK","AIR-LAX"),
           ("AIR-LAX","AIR-SHANGHAI"),("AIR-HONGKONG","AIR-CHANGI"),("AIR-HONGKONG","AIR-DUBAI"),
           ("AIR-DUBAI","AIR-SCHIPHOL"),("AIR-SCHIPHOL","AIR-FRANKFURT"),("AIR-COK","AIR-DUBAI"),
           ("AIR-COK","AIR-DELHI"),("AIR-DUBAI","AIR-MUMBAI")]
    
    # Rail
    RAIL = [("RAIL-ZHENGZHOU","RAIL-XIAN"),("RAIL-XIAN","RAIL-URUMQI"),("RAIL-URUMQI","RAIL-KHORGOS"),
            ("RAIL-KHORGOS","RAIL-ALMATY"),("RAIL-ALMATY","RAIL-MOSCOW"),("RAIL-MOSCOW","RAIL-WARSAW"),
            ("RAIL-WARSAW","RAIL-DUISBURG"),("RAIL-DUISBURG","PORT-ROTTERDAM"),("RAIL-KOCHI","RAIL-NHAVASHEVA"),
            ("RAIL-NHAVASHEVA","RAIL-DELHI"),("RAIL-DELHI","PORT-CHENNAI"),("RAIL-KOCHI","PORT-KOCHI"),
            ("RAIL-LOSANGELES","RAIL-CHICAGO"),("RAIL-CHICAGO","PORT-NEWYORK")]
    
    # Road
    ROAD = [("DC-KOCHI","HUB-MUMBAI"),("HUB-MUMBAI","PORT-MUMBAI"),("HUB-MUMBAI","RAIL-NHAVASHEVA"),
            ("HUB-CHICAGO","RAIL-CHICAGO"),("HUB-DUBAI","PORT-JEBEL"),("HUB-SHANGHAI","PORT-SHANGHAI")]

    # 2. Add connections to each hub
    for hub in hubs:
        hub["connections"] = []
        hid = hub["id"]
        
        # Helper to find connections
        def add_conns(con_list, mode):
            for u, v in con_list:
                if u == hid and v in hub_ids:
                    hub["connections"].append({"to": v, "mode": mode})
                elif v == hid and u in hub_ids:
                    hub["connections"].append({"to": u, "mode": mode})
        
        add_conns(SEA, "sea")
        add_conns(AIR, "air")
        add_conns(RAIL, "rail")
        add_conns(ROAD, "road")

    # 3. Save as single authority
    with open(hubs_path, "w") as f:
        json.dump(hubs, f, indent=2)
        
    print(f"Migration complete: {len(hubs)} hubs now contain connection logic.")

if __name__ == "__main__":
    migrate_to_single_source()
