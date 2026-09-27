#!/usr/bin/env python3
"""Part 4: Final 64 resilience hubs (237-300). Disruption bypass & corridor redundancy."""
import json

RAW4 = [
# === CAPE ROUTE ALTERNATIVES (Suez bypass) ===
("PORT-WALVISBAY","Port of Walvis Bay",["Walvis Bay"],"port",["sea","road","rail"],-22.9576,14.5053,"Namibia",7,"Southern Africa corridor port and Suez bypass staging node"),
("PORT-LUANDA","Port of Luanda",["Luanda"],"port",["sea","road"],-8.8383,13.2344,"Angola",6,"West-Central Africa gateway on Cape Route alternative"),
("PORT-RICHARDSBAY","Port of Richards Bay",["Richards Bay"],"port",["sea","road","rail"],-28.7833,32.0833,"South Africa",7,"Africa's largest bulk port and Cape Route coal/mineral hub"),
("PORT-TOAMASINA","Port of Toamasina",["Toamasina","Tamatave"],"port",["sea","road"],-18.1553,49.3900,"Madagascar",6,"Indian Ocean island hub on Cape-Suez alternative lane"),
# === RED SEA BYPASS / BAB EL-MANDEB ALTERNATIVES ===
("PORT-BERBERA","Port of Berbera",["Berbera"],"port",["sea","road"],10.4394,45.0364,"Somaliland",6,"Horn of Africa alternate to Djibouti on Red Sea approach"),
("PORT-ADEN","Port of Aden",["Aden"],"port",["sea","road"],12.7855,45.0187,"Yemen",7,"Bab el-Mandeb staging port and Red Sea southern alternate"),
("PORT-PORTSUDAN","Port Sudan",["Port Sudan"],"port",["sea","road","rail"],19.6158,37.2164,"Sudan",6,"Red Sea western shore alternate bypassing Suez congestion"),
# === HORMUZ ALTERNATIVES (Gulf bypass) ===
("PORT-FUJAIRAH","Port of Fujairah",["Fujairah"],"port",["sea","road"],25.1164,56.3361,"UAE",8,"UAE's Indian Ocean-facing port bypassing Strait of Hormuz entirely"),
("PORT-DUQM","Port of Duqm",["Duqm"],"port",["sea","road"],19.6614,57.7028,"Oman",7,"Oman mega-port outside Hormuz for sanctions-resilient routing"),
("PORT-GWADAR","Port of Gwadar",["Gwadar","CPEC"],"port",["sea","road"],25.1264,62.3225,"Pakistan",7,"CPEC terminus bypassing Hormuz for China-Pakistan corridor"),
# === ARCTIC / NORTHERN CORRIDOR ===
("PORT-MURMANSK","Port of Murmansk",["Murmansk"],"port",["sea","road","rail"],68.9585,33.0827,"Russia",7,"Arctic shipping route western terminus and Northern Sea Route hub"),
("PORT-ARKHANGELSK","Port of Arkhangelsk",["Arkhangelsk"],"port",["sea","road","rail"],64.5399,40.5152,"Russia",6,"White Sea alternate Arctic port with rail to Moscow"),
("CHOKE-NSR","Northern Sea Route",["NSR","Arctic Route"],"choke_point",["sea"],72.0000,125.0000,"Russia",8,"Arctic corridor alternative to Suez cutting Asia-Europe by 40%"),
# === CENTRAL ASIA RAIL FALLBACK ===
("RAIL-SAMARKAND","Samarkand Rail Junction",["Samarkand"],"rail_hub",["rail","road"],39.6542,66.9597,"Uzbekistan",6,"Uzbek rail junction on Middle Corridor BRI alternate"),
("RAIL-TBILISI","Tbilisi Rail Terminal",["Tbilisi","Georgia Rail"],"rail_hub",["rail","road"],41.7151,44.8271,"Georgia",7,"Trans-Caspian Middle Corridor European anchor"),
("RAIL-AKTAU","Aktau Port-Rail Terminal",["Aktau","Caspian"],"rail_hub",["rail","road","sea"],43.6500,51.1500,"Kazakhstan",7,"Caspian Sea rail-ferry interchange on Middle Corridor"),
("PORT-BAKU","Port of Baku",["Baku Port","Alat"],"port",["sea","road","rail"],40.3700,49.8500,"Azerbaijan",7,"Caspian Sea RoRo hub linking Central Asia to Caucasus rail"),
("RAIL-KARS","Kars Rail Terminal",["Kars","BTK Railway"],"rail_hub",["rail","road"],40.6013,43.0975,"Turkey",7,"Baku-Tbilisi-Kars railway European terminus"),
# === EAST AFRICA INLAND CORRIDORS ===
("RAIL-KAMPALA","Kampala Freight Terminal",["Kampala"],"rail_hub",["rail","road"],0.3476,32.5825,"Uganda",6,"Northern Corridor inland terminus for landlocked East Africa"),
("RAIL-KIGALI","Kigali Logistics Hub",["Kigali"],"distribution_hub",["road"],-1.9403,29.8739,"Rwanda",5,"Central Africa distribution node and Great Lakes logistics anchor"),
("HUB-DARES","Dar es Salaam Logistics Zone",["DSM Logistics"],"distribution_hub",["road","rail"],-6.8000,39.2800,"Tanzania",6,"Central Corridor inland freight staging area"),
# === US-MEXICO BORDER ALTERNATES ===
("BORDER-NOGALES","Nogales Border Crossing",["Nogales","Mariposa"],"distribution_hub",["road"],31.3382,-110.9375,"USA",6,"Arizona-Sonora produce corridor and USMCA alternate crossing"),
("BORDER-BROWNSVILLE","Brownsville-Matamoros Gateway",["Brownsville","Veterans Bridge"],"distribution_hub",["road","rail"],25.9017,-97.4975,"USA",7,"Easternmost US-Mexico crossing with rail and deep-water port access"),
("PORT-BROWNSVILLE","Port of Brownsville",["Brownsville Port"],"port",["sea","road","rail"],25.9700,-97.3900,"USA",6,"Gulf alternate to Houston for Mexico nearshoring freight"),
# === SOUTH AMERICA PACIFIC-ATLANTIC BRIDGES ===
("RAIL-MENDOZA","Mendoza Trans-Andean Rail",["Mendoza"],"rail_hub",["rail","road"],-32.8895,-68.8458,"Argentina",6,"Trans-Andean freight corridor connecting Atlantic Argentina to Pacific Chile"),
("PORT-ARICA","Port of Arica",["Arica"],"port",["sea","road","rail"],-18.4783,-70.3126,"Chile",6,"Pacific gateway for landlocked Bolivia and Peru alternate"),
("PORT-IQUIQUE","Port of Iquique",["Iquique","ZOFRI"],"port",["sea","road"],-20.2133,-70.1500,"Chile",6,"Northern Chile free zone port and Pacific-Atlantic bridge node"),
("PORT-PARANAGUA2","Antonina Port Complex",["Antonina"],"port",["sea","road"],-25.4333,-48.7167,"Brazil",5,"Santos overflow port and Parana state alternate export gateway"),
# === SECONDARY AIR CARGO FALLBACK HUBS ===
("AIR-HAHN","Frankfurt-Hahn Airport",["HHN","Hahn"],"airport",["air","road"],49.9487,7.2639,"Germany",6,"European low-cost cargo alternate when Frankfurt is congested"),
("AIR-SHARJAH2","Sharjah Cargo Village",["SHJ Cargo"],"airport",["air","road"],25.3300,55.5200,"UAE",6,"Dubai overflow cargo facility for peak season resilience"),
("AIR-RICKENBACKER","Rickenbacker Cargo Airport",["LCK","Rickenbacker"],"airport",["air","road"],39.8138,-82.9272,"USA",7,"US Midwest dedicated cargo airport alternate to O'Hare"),
("AIR-LIEGE2","Liege Bierset Cargo",["Bierset"],"airport",["air","road"],50.6400,5.4500,"Belgium",6,"European e-commerce overflow hub alternate to Leipzig"),
("AIR-ALMATY","Almaty International Airport",["ALA","Almaty Air"],"airport",["air","road"],43.3521,77.0405,"Kazakhstan",6,"Central Asia air cargo hub on Middle Corridor air bridge"),
# === RAIL BYPASS / SANCTIONS RESILIENCE ===
("RAIL-BREST","Brest Rail Terminal",["Brest","Belarus Border"],"rail_hub",["rail","road"],52.0977,23.7341,"Belarus",7,"EU-CIS gauge change point and BRI European border interchange"),
("RAIL-ILETSK","Iletsk Rail Junction",["Iletsk","Orenburg"],"rail_hub",["rail","road"],51.3556,54.6939,"Russia",6,"Russia-Kazakhstan rail border bypass for sanctions routing"),
("RAIL-DOSTYK","Dostyk Border Terminal",["Dostyk","Druzhba"],"rail_hub",["rail","road"],45.4833,82.5000,"Kazakhstan",7,"China-Kazakhstan alternate gauge-change to Khorgos"),
("RAIL-MANZHOULI","Manzhouli Border Station",["Manzhouli","满洲里"],"rail_hub",["rail","road"],49.5978,117.3787,"China",7,"China-Russia direct rail border crossing bypassing Central Asia"),
("RAIL-SUZHOU","Suzhou West Rail Port",["Suzhou Rail"],"rail_hub",["rail","road"],31.2989,120.5853,"China",6,"Yangtze Delta BRI origin alternate to Zhengzhou/Yiwu"),
# === STRATEGIC CONNECTORS ===
("PORT-PORTSAID2","East Port Said Industrial Zone",["East Port Said"],"distribution_hub",["road","sea"],31.2800,32.3200,"Egypt",7,"Suez Canal adjacent logistics park and transshipment staging area"),
("HUB-JEBEL","Jebel Ali Free Zone",["JAFZA Hub"],"distribution_hub",["road","sea"],25.0200,55.0800,"UAE",8,"World's largest free zone adjacent to Jebel Ali port"),
("PORT-HAMBANTOTA","Hambantota Port",["Hambantota"],"port",["sea","road"],6.1190,81.1033,"Sri Lanka",6,"Chinese-built Indian Ocean deep-water alternate to Colombo"),
("PORT-TRINCOMALEE","Port of Trincomalee",["Trincomalee"],"port",["sea","road"],8.5833,81.2333,"Sri Lanka",5,"Indian Ocean natural harbor alternate and naval logistics node"),
("HUB-DAMMAM","King Abdulaziz Port Dammam",["Dammam","KAAP"],"distribution_hub",["road","rail","sea"],26.4207,50.0888,"Saudi Arabia",7,"Persian Gulf industrial port bypassing Hormuz via pipeline corridor"),
("PORT-TANJUNGSAUH","Tanjung Sauh Anchorage",["Batam","Tanjung Sauh"],"port",["sea","road"],1.0500,104.1000,"Indonesia",6,"Singapore Strait alternate anchorage for Malacca overflow"),
("PORT-CAIMEP","Cai Mep International Terminal",["Cai Mep","CMIT"],"port",["sea","road"],10.4800,107.0100,"Vietnam",7,"Vietnam deep-water alternate to HCMC for mega-vessel direct calls"),
# === ADDITIONAL RESILIENCE NODES (to reach 300) ===
("HUB-LILLE","Lille Logistics Hub",["Lille","CRT Lesquin"],"distribution_hub",["road","rail"],50.6292,3.0573,"France",7,"Northern France rail-road crossroads for UK-EU-Benelux trade"),
("HUB-BOLOGNA","Bologna Interporto",["Interporto Bologna"],"distribution_hub",["road","rail"],44.4949,11.3426,"Italy",7,"Italy's primary intermodal terminal for North-South freight"),
("RAIL-VERONA","Verona Quadrante Europa",["Verona Rail"],"rail_hub",["rail","road"],45.4384,10.9916,"Italy",7,"Europe's most active intermodal hub for Alpine transit"),
("RAIL-MALASZEWICZE","Malaszewicze Rail Terminal",["Malaszewicze"],"rail_hub",["rail","road"],52.0300,23.5100,"Poland",8,"The 'Gateway to Europe' for China-Europe rail freight"),
("HUB-DUISBURG","Duisburg Logport",["Logport"],"distribution_hub",["road","rail","sea"],51.4344,6.7623,"Germany",8,"World's largest inland port and BRI European terminus cluster"),
("PORT-RAVENNA","Port of Ravenna",["Ravenna"],"port",["sea","road","rail"],44.4183,12.2035,"Italy",6,"Adriatic alternate to Venice/Trieste for Balkan trade"),
("AIR-OSLO","Oslo Gardermoen Cargo",["OSL"],"airport",["air","road"],60.1975,11.1004,"Norway",6,"Nordic air cargo hub for seafood exports and Arctic logistics"),
("PORT-NARVIK","Port of Narvik",["Narvik"],"port",["sea","road","rail"],68.4385,17.4272,"Norway",6,"Ice-free Arctic port with heavy rail link to Sweden"),
("HUB-STOCKHOLM","Stockholm Logistics Hub",["Stockholm","Arlanda Logistics"],"distribution_hub",["road","rail","air"],59.3293,18.0686,"Sweden",7,"Baltic-Nordic logistics gateway"),
("PORT-HELSINKI","Port of Helsinki Vuosaari",["Helsinki"],"port",["sea","road","rail"],60.1695,24.9354,"Finland",7,"Finland's primary container gateway"),
("RAIL-HELSINKI","Helsinki Rail Freight",["Pasila Rail"],"rail_hub",["rail","road"],60.2000,24.9300,"Finland",6,"Northernmost BRI rail link terminus"),
("PORT-REYKJAVIK","Port of Reykjavik",["Reykjavik"],"port",["sea","road"],64.1265,-21.8271,"Iceland",6,"North Atlantic mid-point for US-Europe Arctic routes"),
("AIR-ANCHORAGE2","PANC Cargo Hub",["Anchorage Air"],"airport",["air","road"],61.1744,-149.9962,"USA",8,"Strategic Trans-Pacific air cargo refueling and sorting hub"),
("PORT-PRINCE_RUPERT","Port of Prince Rupert",["Prince Rupert"],"port",["sea","road","rail"],54.3122,-130.3271,"Canada",8,"North America's fastest growing Pacific container gateway"),
("RAIL-PRINCE_RUPERT","Prince Rupert Rail Terminal",["CN Prince Rupert"],"rail_hub",["rail","road"],54.3000,-130.3000,"Canada",7,"Deep-water rail-port interface for Asian trade to US Midwest"),
("PORT-HALIFAX","Port of Halifax",["Halifax"],"port",["sea","road","rail"],44.6488,-63.5752,"Canada",7,"Atlantic Canada's primary container and automotive port"),
("RAIL-WINNIPEG","Winnipeg CentrePort Canada",["Winnipeg","CentrePort"],"rail_hub",["rail","road","air"],49.8951,-97.1384,"Canada",7,"North America's largest tri-modal inland port"),
("HUB-CHICAGO","Elk Grove Village Logistics",["Elk Grove","ORD Logistics"],"distribution_hub",["road","rail","air"],42.0039,-87.9973,"USA",8,"US Midwest primary data center and e-commerce cluster"),
("PORT-CHARLESTON","Port of Charleston",["Charleston"],"port",["sea","road","rail"],32.7765,-79.9309,"USA",8,"US Southeast high-efficiency deep-water port"),
]

def build_hub(r):
    return {"id":r[0],"display_name":r[1],"aliases":r[2],"type":r[3],"modes":r[4],
            "lat":r[5],"lon":r[6],"country":r[7],"importance":r[8],"strategic_role":r[9]}

if __name__ == "__main__":
    with open("backend/data/canonical_hubs.json","r") as f:
        existing = json.load(f)
    existing_ids = {h["id"] for h in existing}
    new_hubs = [build_hub(r) for r in RAW4]
    
    # Filter out duplicates
    unique_new = []
    for h in new_hubs:
        if h["id"] not in existing_ids:
            unique_new.append(h)
            existing_ids.add(h["id"])
            
    merged = existing + unique_new
    with open("backend/data/canonical_hubs.json","w") as f:
        json.dump(merged, f, indent=2)

    types = {}
    for h in merged:
        types[h["type"]] = types.get(h["type"], 0) + 1
    
    print(f"Part 4 complete. Added: {len(unique_new)}. Total: {len(merged)}")
    for t, c in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t:20s} {c:3d} ({c/len(merged)*100:.1f}%)")

    report = {"total": len(merged), "part4_added": len(unique_new), "types": types}
    with open("backend/data/validation_report.json", "w") as f:
        json.dump(report, f, indent=2)
