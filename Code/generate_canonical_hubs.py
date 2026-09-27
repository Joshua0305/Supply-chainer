import json
import os

HUBS = [
    # --- MAJOR PORTS ---
    {"id": "CNSHG", "display_name": "Port of Shanghai", "aliases": ["Shanghai", "Yangshan"], "type": "port", "modes": ["sea", "road", "rail"], "lat": 31.2304, "lon": 121.4737, "country": "China", "importance": 100},
    {"id": "SGSIN", "display_name": "Port of Singapore", "aliases": ["Singapore", "Jurong"], "type": "port", "modes": ["sea", "road"], "lat": 1.3521, "lon": 103.8198, "country": "Singapore", "importance": 100},
    {"id": "NLRTM", "display_name": "Port of Rotterdam", "aliases": ["Rotterdam", "Europoort"], "type": "port", "modes": ["sea", "road", "rail"], "lat": 51.9225, "lon": 4.4792, "country": "Netherlands", "importance": 95},
    {"id": "USLAX", "display_name": "Port of Los Angeles", "aliases": ["Los Angeles", "LA Port"], "type": "port", "modes": ["sea", "road", "rail"], "lat": 34.0522, "lon": -118.2437, "country": "USA", "importance": 90},
    {"id": "USLGB", "display_name": "Port of Long Beach", "aliases": ["Long Beach"], "type": "port", "modes": ["sea", "road", "rail"], "lat": 33.7701, "lon": -118.1937, "country": "USA", "importance": 85},
    {"id": "AEJEA", "display_name": "Jebel Ali Port", "aliases": ["Dubai Port", "Jebel Ali"], "type": "port", "modes": ["sea", "road"], "lat": 25.0112, "lon": 55.0612, "country": "UAE", "importance": 90},
    {"id": "INBOM", "display_name": "Jawaharlal Nehru Port (JNPT)", "aliases": ["Mumbai Port", "Nhava Sheva"], "type": "port", "modes": ["sea", "road", "rail"], "lat": 18.95, "lon": 72.95, "country": "India", "importance": 85},
    {"id": "INKCH", "display_name": "Port of Kochi", "aliases": ["Kochi Port", "Cochin"], "type": "port", "modes": ["sea", "road", "rail"], "lat": 9.9312, "lon": 76.2673, "country": "India", "importance": 80},
    {"id": "INMAA", "display_name": "Chennai Port", "aliases": ["Chennai"], "type": "port", "modes": ["sea", "road", "rail"], "lat": 13.0827, "lon": 80.2707, "country": "India", "importance": 80},
    {"id": "USNYC", "display_name": "Port of New York & New Jersey", "aliases": ["New York Port", "Newark"], "type": "port", "modes": ["sea", "road", "rail"], "lat": 40.7128, "lon": -74.0060, "country": "USA", "importance": 90},
    {"id": "DEHAM", "display_name": "Port of Hamburg", "aliases": ["Hamburg"], "type": "port", "modes": ["sea", "road", "rail"], "lat": 53.5511, "lon": 9.9937, "country": "Germany", "importance": 85},
    {"id": "HKHKG", "display_name": "Port of Hong Kong", "aliases": ["Hong Kong Port", "Kwai Tsing"], "type": "port", "modes": ["sea", "road"], "lat": 22.3193, "lon": 114.1694, "country": "Hong Kong", "importance": 90},
    {"id": "KRPUS", "display_name": "Port of Busan", "aliases": ["Busan"], "type": "port", "modes": ["sea", "road", "rail"], "lat": 35.1796, "lon": 129.0756, "country": "South Korea", "importance": 90},
    
    # --- MAJOR CARGO AIRPORTS ---
    {"id": "AIR-HKG", "display_name": "Hong Kong International Airport", "aliases": ["HKG", "Chek Lap Kok"], "type": "airport", "modes": ["air", "road"], "lat": 22.3080, "lon": 113.9185, "country": "Hong Kong", "importance": 100},
    {"id": "AIR-MEM", "display_name": "Memphis International Airport", "aliases": ["MEM", "FedEx Hub"], "type": "airport", "modes": ["air", "road"], "lat": 35.0423, "lon": -89.9792, "country": "USA", "importance": 95},
    {"id": "AIR-PVG", "display_name": "Shanghai Pudong International", "aliases": ["PVG"], "type": "airport", "modes": ["air", "road"], "lat": 31.1443, "lon": 121.8083, "country": "China", "importance": 95},
    {"id": "AIR-ANC", "display_name": "Ted Stevens Anchorage International", "aliases": ["ANC", "Anchorage"], "type": "airport", "modes": ["air", "road"], "lat": 61.1743, "lon": -149.9963, "country": "USA", "importance": 90},
    {"id": "AIR-DXB", "display_name": "Dubai International Airport", "aliases": ["DXB"], "type": "airport", "modes": ["air", "road"], "lat": 25.2532, "lon": 55.3657, "country": "UAE", "importance": 95},
    {"id": "AIR-DEL", "display_name": "Indira Gandhi International Airport", "aliases": ["DEL", "Delhi Air Cargo"], "type": "airport", "modes": ["air", "road"], "lat": 28.5562, "lon": 77.1000, "country": "India", "importance": 85},
    {"id": "AIR-FRA", "display_name": "Frankfurt Airport", "aliases": ["FRA", "Lufthansa Cargo"], "type": "airport", "modes": ["air", "road", "rail"], "lat": 50.0379, "lon": 8.5622, "country": "Germany", "importance": 90},
    {"id": "AIR-ORD", "display_name": "Chicago O'Hare International", "aliases": ["ORD", "Chicago Air"], "type": "airport", "modes": ["air", "road", "rail"], "lat": 41.9742, "lon": -87.9073, "country": "USA", "importance": 90},
    {"id": "AIR-ATL", "display_name": "Hartsfield-Jackson Atlanta", "aliases": ["ATL", "Atlanta Air"], "type": "airport", "modes": ["air", "road"], "lat": 33.6407, "lon": -84.4277, "country": "USA", "importance": 85},
    
    # --- STRATEGIC CHOKE POINTS ---
    {"id": "CHOKE-SUEZ", "display_name": "Suez Canal", "aliases": ["Suez", "Egypt"], "type": "choke_point", "modes": ["sea"], "lat": 30.5852, "lon": 32.2654, "country": "Egypt", "importance": 100},
    {"id": "CHOKE-PANAMA", "display_name": "Panama Canal", "aliases": ["Panama"], "type": "choke_point", "modes": ["sea"], "lat": 9.1450, "lon": -79.6664, "country": "Panama", "importance": 100},
    {"id": "CHOKE-MALACCA", "display_name": "Strait of Malacca", "aliases": ["Malacca"], "type": "choke_point", "modes": ["sea"], "lat": 2.1667, "lon": 102.2500, "country": "Malaysia/Indonesia", "importance": 100},
    {"id": "CHOKE-HORMUZ", "display_name": "Strait of Hormuz", "aliases": ["Hormuz"], "type": "choke_point", "modes": ["sea"], "lat": 26.5667, "lon": 56.2500, "country": "Oman/Iran", "importance": 100},
    
    # --- MAJOR RAIL & DISTRIBUTION HUBS ---
    {"id": "RAIL-CHI", "display_name": "Chicago Rail Hub", "aliases": ["Chicago Rail", "BNSF Corwith"], "type": "rail", "modes": ["rail", "road"], "lat": 41.8781, "lon": -87.6298, "country": "USA", "importance": 95},
    {"id": "RAIL- Zhengzhou", "display_name": "Zhengzhou International Hub", "aliases": ["Zhengzhou", "Silk Road Rail"], "type": "rail", "modes": ["rail", "road"], "lat": 34.7466, "lon": 113.6253, "country": "China", "importance": 90},
    {"id": "RAIL-DUIS", "display_name": "Duisburg Intermodal Terminal", "aliases": ["Duisburg", "Duisport"], "type": "rail", "modes": ["rail", "road", "sea"], "lat": 51.4344, "lon": 6.7623, "country": "Germany", "importance": 90},
    {"id": "HUB-DAL", "display_name": "Dallas Logistics Corridor", "aliases": ["Dallas Hub", "AllianceTexas"], "type": "distribution_hub", "modes": ["road", "rail", "air"], "lat": 32.7767, "lon": -96.7970, "country": "USA", "importance": 85},
    {"id": "HUB-DXB", "display_name": "Dubai Logistics City", "aliases": ["DLC", "Dubai South"], "type": "distribution_hub", "modes": ["road", "air", "sea"], "lat": 24.8966, "lon": 55.1500, "country": "UAE", "importance": 90}
]

def generate():
    os.makedirs('backend/data', exist_ok=True)
    with open('backend/data/canonical_hubs.json', 'w') as f:
        json.dump(HUBS, f, indent=4)
    print(f"Generated {len(HUBS)} canonical hubs.")

if __name__ == "__main__":
    generate()
