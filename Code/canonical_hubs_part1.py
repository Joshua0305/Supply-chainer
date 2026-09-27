#!/usr/bin/env python3
"""Part 1: First 100 Strategic Logistics Hubs for Supplychainer Canonical Registry."""
# Format: (id, name, aliases, type, modes, lat, lon, country, importance, role)
RAW = [
# === STRATEGIC CHOKE POINTS ===
("CHOKE-SUEZ","Suez Canal",["Suez","Egypt Canal"],"choke_point",["sea"],30.5852,32.2654,"Egypt",10,"Critical Europe-Asia maritime chokepoint handling 12% of global trade"),
("CHOKE-PANAMA","Panama Canal",["Panama"],"choke_point",["sea"],9.1450,-79.6664,"Panama",10,"Atlantic-Pacific transit corridor handling 6% of global seaborne trade"),
("CHOKE-MALACCA","Strait of Malacca",["Malacca"],"choke_point",["sea"],2.1667,102.2500,"Malaysia",10,"Primary East Asia-Indian Ocean chokepoint for 25% of global shipping"),
("CHOKE-HORMUZ","Strait of Hormuz",["Hormuz"],"choke_point",["sea"],26.5667,56.2500,"Oman",10,"Critical oil/LNG transit corridor between Persian Gulf and Indian Ocean"),
("CHOKE-BABEL","Bab el-Mandeb Strait",["Bab el-Mandeb","Red Sea Gate"],"choke_point",["sea"],12.5833,43.3333,"Djibouti",10,"Red Sea-Indian Ocean gateway controlling Suez approach traffic"),
("CHOKE-BOSPHO","Bosphorus Strait",["Turkish Straits","Istanbul Strait"],"choke_point",["sea"],41.1194,29.0611,"Turkey",9,"Black Sea-Mediterranean transit corridor for grain and energy exports"),
("CHOKE-GIBRAL","Strait of Gibraltar",["Gibraltar"],"choke_point",["sea"],35.9667,-5.6000,"Spain",9,"Atlantic-Mediterranean gateway handling major container and energy flows"),
("CHOKE-DOVER","Dover Strait",["English Channel"],"choke_point",["sea"],51.0500,1.4500,"UK",8,"Busiest shipping lane globally connecting North Sea to Atlantic"),
# === MAJOR SEAPORTS - ASIA ===
("PORT-SHANGHAI","Port of Shanghai",["Shanghai","Yangshan"],"port",["sea","road","rail"],31.2304,121.4737,"China",10,"World's largest container port by TEU throughput"),
("PORT-SINGAPORE","Port of Singapore",["Singapore","Jurong","PSA"],"port",["sea","road"],1.2644,103.8198,"Singapore",10,"World's premier transshipment hub at Malacca Strait junction"),
("PORT-NINGBO","Port of Ningbo-Zhoushan",["Ningbo","Zhoushan"],"port",["sea","road","rail"],29.8683,121.5440,"China",9,"Third largest global container port serving Yangtze Delta manufacturing"),
("PORT-SHENZHEN","Port of Shenzhen",["Shenzhen","Yantian","Shekou"],"port",["sea","road","rail"],22.4784,114.0672,"China",9,"Primary export gateway for Pearl River Delta manufacturing zone"),
("PORT-GUANGZHOU","Port of Guangzhou",["Guangzhou","Nansha"],"port",["sea","road","rail"],22.6280,113.5842,"China",9,"Major South China container and bulk cargo hub"),
("PORT-QINGDAO","Port of Qingdao",["Qingdao"],"port",["sea","road","rail"],36.0671,120.3826,"China",8,"Key North China gateway and crude oil import terminal"),
("PORT-TIANJIN","Port of Tianjin",["Tianjin","Xingang"],"port",["sea","road","rail"],38.9860,117.7279,"China",8,"Beijing's primary maritime gateway and bulk cargo terminal"),
("PORT-HONGKONG","Port of Hong Kong",["Hong Kong","Kwai Tsing"],"port",["sea","road"],22.3193,114.1694,"Hong Kong",9,"Major transshipment and financial trade hub in South China Sea"),
("PORT-BUSAN","Port of Busan",["Busan","Pusan"],"port",["sea","road","rail"],35.0796,129.0440,"South Korea",9,"Northeast Asia transshipment hub and Korea's primary container port"),
("PORT-KAOHSIUNG","Port of Kaohsiung",["Kaohsiung","Taiwan"],"port",["sea","road","rail"],22.6155,120.2930,"Taiwan",8,"Taiwan's largest port and East Asia feeder hub"),
("PORT-TOKYO","Port of Tokyo",["Tokyo","Oi"],"port",["sea","road","rail"],35.6214,139.7753,"Japan",8,"Japan's primary container import gateway for Greater Tokyo"),
("PORT-YOKOHAMA","Port of Yokohama",["Yokohama"],"port",["sea","road","rail"],35.4534,139.6380,"Japan",8,"Major Japanese auto export and container terminal"),
("PORT-LAEMCHA","Laem Chabang Port",["Laem Chabang","Thailand"],"port",["sea","road","rail"],13.0827,100.8839,"Thailand",8,"Thailand's primary deep-sea container port and Eastern Seaboard hub"),
("PORT-HOCHIMINH","Ho Chi Minh City Port",["HCMC Port","Cat Lai","Saigon"],"port",["sea","road"],10.7553,106.7536,"Vietnam",8,"Vietnam's largest container port serving southern manufacturing"),
("PORT-PORTKLANG","Port Klang",["Port Klang","Westport","Northport"],"port",["sea","road","rail"],2.9986,101.3900,"Malaysia",8,"Malaysia's busiest port and Malacca Strait transshipment node"),
("PORT-TPELEPAS","Tanjung Pelepas Port",["Tanjung Pelepas","PTP"],"port",["sea","road"],1.3667,103.5500,"Malaysia",8,"Major Maersk/MSC transshipment hub at southern Malacca Strait"),
("PORT-COLOMBO","Port of Colombo",["Colombo"],"port",["sea","road"],6.9404,79.8428,"Sri Lanka",8,"Indian Ocean transshipment hub on Asia-Europe mainline route"),
# === MAJOR SEAPORTS - INDIA ===
("PORT-MUMBAI","Jawaharlal Nehru Port (JNPT)",["Mumbai Port","JNPT","Nhava Sheva","Bombay"],"port",["sea","road","rail"],18.9500,72.9500,"India",9,"India's largest container port handling 50%+ of containerized cargo"),
("PORT-MUNDRA","Port of Mundra",["Mundra","Adani Port"],"port",["sea","road","rail"],22.7390,69.7190,"India",8,"India's largest private port and fastest growing container terminal"),
("PORT-CHENNAI","Chennai Port",["Chennai","Madras Port"],"port",["sea","road","rail"],13.0827,80.2707,"India",8,"East Coast India's primary container and auto cargo gateway"),
("PORT-KOCHI","Port of Kochi",["Kochi","Cochin","Vallarpadam"],"port",["sea","road","rail"],9.9312,76.2673,"India",7,"Strategic transshipment hub on India's southwest coast"),
("PORT-VIZAG","Visakhapatnam Port",["Vizag","Visakhapatnam"],"port",["sea","road","rail"],17.6868,83.2185,"India",7,"Major East Coast bulk and container port"),
("PORT-KANDLA","Deendayal Port (Kandla)",["Kandla","Deendayal"],"port",["sea","road","rail"],23.0225,70.2167,"India",7,"India's largest cargo tonnage port on Gulf of Kutch"),
# === MAJOR SEAPORTS - MIDDLE EAST & AFRICA ===
("PORT-JEBEL","Jebel Ali Port",["Jebel Ali","Dubai Port","DP World"],"port",["sea","road"],25.0112,55.0612,"UAE",9,"World's largest man-made port and Middle East logistics hub"),
("PORT-JEDDAH","Jeddah Islamic Port",["Jeddah","King Abdullah Port"],"port",["sea","road"],21.4858,39.1925,"Saudi Arabia",8,"Red Sea's primary container and Hajj logistics gateway"),
("PORT-SALALAH","Port of Salalah",["Salalah"],"port",["sea","road"],16.9400,54.0000,"Oman",7,"Arabian Sea transshipment hub on Asia-Europe mainline"),
("PORT-DJIBOUTI","Port of Djibouti",["Djibouti","Doraleh"],"port",["sea","road","rail"],11.5945,43.1456,"Djibouti",8,"Horn of Africa gateway and Bab el-Mandeb transit staging hub"),
("PORT-DURBAN","Port of Durban",["Durban"],"port",["sea","road","rail"],-29.8687,31.0480,"South Africa",8,"Africa's busiest container port and sub-Saharan logistics hub"),
("PORT-TANGIER","Tanger Med Port",["Tangier Med","Tanger"],"port",["sea","road","rail"],35.8838,-5.4950,"Morocco",8,"Africa's largest port and Mediterranean transshipment gateway"),
("PORT-MOMBASA","Port of Mombasa",["Mombasa"],"port",["sea","road","rail"],-4.0435,39.6682,"Kenya",7,"East Africa's primary maritime gateway and landlocked nations corridor"),
# === MAJOR SEAPORTS - EUROPE ===
("PORT-ROTTERDAM","Port of Rotterdam",["Rotterdam","Europoort","Maasvlakte"],"port",["sea","road","rail"],51.9225,4.4792,"Netherlands",10,"Europe's largest port and primary Atlantic gateway"),
("PORT-ANTWERP","Port of Antwerp-Bruges",["Antwerp","Antwerpen"],"port",["sea","road","rail"],51.2994,4.3571,"Belgium",9,"Europe's second largest port and chemical cargo hub"),
("PORT-HAMBURG","Port of Hamburg",["Hamburg"],"port",["sea","road","rail"],53.5329,9.9662,"Germany",9,"Germany's largest port and Northern Europe distribution gateway"),
("PORT-FELIXSTOWE","Port of Felixstowe",["Felixstowe"],"port",["sea","road","rail"],51.9558,1.3513,"UK",8,"UK's largest container port handling 40% of national trade"),
("PORT-PIRAEUS","Port of Piraeus",["Piraeus","Athens Port"],"port",["sea","road","rail"],37.9430,23.6388,"Greece",8,"Mediterranean hub and COSCO's Europe gateway from Suez"),
("PORT-VALENCIA","Port of Valencia",["Valencia"],"port",["sea","road","rail"],39.4420,-0.3240,"Spain",8,"Spain's largest container port and Western Med gateway"),
("PORT-LEHAVRE","Port of Le Havre",["Le Havre"],"port",["sea","road","rail"],49.4814,0.1069,"France",7,"France's primary container port on English Channel approach"),
("PORT-GDANSK","Port of Gdansk",["Gdansk","DCT Gdansk"],"port",["sea","road","rail"],54.3888,18.6623,"Poland",7,"Baltic's fastest growing deep-sea container terminal"),
("PORT-GOTHENBURG","Port of Gothenburg",["Gothenburg"],"port",["sea","road","rail"],57.6888,11.9350,"Sweden",7,"Scandinavia's largest port and Nordic distribution gateway"),
# === MAJOR SEAPORTS - AMERICAS ===
("PORT-LOSANGELES","Port of Los Angeles",["Los Angeles","San Pedro","LA Port"],"port",["sea","road","rail"],33.7361,-118.2631,"USA",9,"Western Hemisphere's busiest container port complex"),
("PORT-LONGBEACH","Port of Long Beach",["Long Beach"],"port",["sea","road","rail"],33.7544,-118.2167,"USA",9,"US second busiest container port adjacent to LA complex"),
("PORT-NEWYORK","Port of New York & New Jersey",["New York Port","Newark","PONYNJ"],"port",["sea","road","rail"],40.6681,-74.1485,"USA",9,"US East Coast's largest container port complex"),
("PORT-SAVANNAH","Port of Savannah",["Savannah","Garden City"],"port",["sea","road","rail"],32.0835,-81.0998,"USA",8,"Fastest growing US East Coast port with rail connectivity"),
("PORT-HOUSTON","Port of Houston",["Houston","Barbours Cut"],"port",["sea","road","rail"],29.7260,-95.2688,"USA",8,"US Gulf Coast's primary container and petrochemical port"),
("PORT-VANCOUVER","Port of Vancouver",["Vancouver","Deltaport"],"port",["sea","road","rail"],49.2827,-123.1207,"Canada",8,"Canada's largest port and Pacific Gateway to North America"),
("PORT-SANTOS","Port of Santos",["Santos"],"port",["sea","road","rail"],-23.9608,-46.3047,"Brazil",8,"Latin America's largest container port and Brazil's trade gateway"),
("PORT-COLON","Port of Colon",["Colon","Cristobal","MIT"],"port",["sea","road"],9.3592,-79.9006,"Panama",8,"Caribbean-side Panama Canal hub and Americas transshipment center"),
("PORT-MANZANILLO","Port of Manzanillo",["Manzanillo Mexico"],"port",["sea","road","rail"],19.0522,-104.3158,"Mexico",7,"Mexico's Pacific coast primary container port"),
("PORT-CHARLESTON","Port of Charleston",["Charleston"],"port",["sea","road","rail"],32.7765,-79.9311,"USA",7,"Major US Southeast container port with deep-water access"),
# === CARGO AIRPORTS ===
("AIR-HONGKONG","Hong Kong International Airport",["HKG","Chek Lap Kok"],"airport",["air","road"],22.3080,113.9185,"Hong Kong",10,"World's busiest air cargo hub by international freight tonnes"),
("AIR-MEMPHIS","Memphis International Airport",["MEM","FedEx SuperHub"],"airport",["air","road"],35.0423,-89.9792,"USA",10,"FedEx global superhub and world's second busiest cargo airport"),
("AIR-SHANGHAI","Shanghai Pudong International",["PVG","Pudong"],"airport",["air","road"],31.1443,121.8083,"China",9,"China's primary international air cargo gateway"),
("AIR-INCHEON","Incheon International Airport",["ICN","Seoul Incheon"],"airport",["air","road","rail"],37.4602,126.4407,"South Korea",9,"Northeast Asia's premier air cargo transshipment hub"),
("AIR-ANCHORAGE","Ted Stevens Anchorage Intl",["ANC","Anchorage"],"airport",["air","road"],61.1743,-149.9963,"USA",9,"Strategic polar route refueling and cargo sorting hub"),
("AIR-DUBAI","Dubai International Airport",["DXB","Dubai Air"],"airport",["air","road"],25.2532,55.3657,"UAE",9,"Middle East's primary air cargo hub connecting three continents"),
("AIR-DWC","Al Maktoum International",["DWC","Dubai World Central"],"airport",["air","road"],24.8966,55.1614,"UAE",8,"Dubai's dedicated cargo mega-airport and free trade zone"),
("AIR-LOUISVILLE","Louisville Muhammad Ali Intl",["SDF","UPS Worldport"],"airport",["air","road"],38.1744,-85.7360,"USA",9,"UPS global air hub and Americas sorting mega-facility"),
("AIR-NARITA","Narita International Airport",["NRT","Tokyo Narita"],"airport",["air","road","rail"],35.7720,140.3929,"Japan",8,"Japan's primary international air cargo terminal"),
("AIR-TAIPEI","Taoyuan International Airport",["TPE","Taiwan Taoyuan"],"airport",["air","road"],25.0797,121.2342,"Taiwan",8,"East Asia high-tech cargo hub and transshipment gateway"),
("AIR-CHANGI","Singapore Changi Airport",["SIN","Changi"],"airport",["air","road"],1.3644,103.9915,"Singapore",9,"Southeast Asia's premier air cargo and pharma hub"),
("AIR-FRANKFURT","Frankfurt Airport",["FRA","Fraport"],"airport",["air","road","rail"],50.0379,8.5622,"Germany",9,"Europe's largest air cargo hub and Lufthansa freight gateway"),
("AIR-SCHIPHOL","Amsterdam Schiphol Airport",["AMS","Schiphol"],"airport",["air","road","rail"],52.3105,4.7683,"Netherlands",8,"Europe's third largest cargo airport and pharma corridor"),
("AIR-CDGPARIS","Paris Charles de Gaulle",["CDG","Roissy"],"airport",["air","road","rail"],49.0097,2.5479,"France",8,"France's primary cargo airport and European e-commerce hub"),
("AIR-HEATHROW","London Heathrow Airport",["LHR","Heathrow"],"airport",["air","road","rail"],51.4700,-0.4543,"UK",8,"UK's primary air cargo gateway for high-value freight"),
("AIR-LEIPZIG","Leipzig/Halle Airport",["LEJ","DHL Hub"],"airport",["air","road","rail"],51.4324,12.2416,"Germany",8,"DHL Express European superhub and e-commerce fulfillment center"),
("AIR-LIEGE","Liège Airport",["LGG","Liège Cargo"],"airport",["air","road"],50.6374,5.4432,"Belgium",7,"Europe's seventh largest cargo airport and Alibaba e-hub"),
("AIR-DOHA","Hamad International Airport",["DOH","Doha"],"airport",["air","road"],25.2731,51.6081,"Qatar",8,"Qatar Airways cargo hub and Middle East-Asia air bridge"),
("AIR-ISTANBUL","Istanbul Airport",["IST"],"airport",["air","road","rail"],41.2753,28.7519,"Turkey",8,"Turkish Cargo hub connecting Europe-Asia-Africa air freight"),
("AIR-DELHI","Indira Gandhi International",["DEL","Delhi Air Cargo","IGI"],"airport",["air","road"],28.5562,77.1000,"India",8,"India's largest air cargo hub and North India gateway"),
("AIR-MUMBAI","Chhatrapati Shivaji Maharaj Intl",["BOM","Mumbai Air"],"airport",["air","road"],19.0896,72.8656,"India",8,"India's primary international air freight terminal"),
("AIR-BANGALORE","Kempegowda International",["BLR","Bangalore Air"],"airport",["air","road"],13.1979,77.7063,"India",7,"India's tech export and pharma air cargo hub"),
("AIR-MIAMI","Miami International Airport",["MIA","Miami Air"],"airport",["air","road"],25.7959,-80.2870,"USA",8,"Americas perishable cargo hub and Latin America gateway"),
("AIR-CHICAGO","Chicago O'Hare International",["ORD","O'Hare"],"airport",["air","road","rail"],41.9742,-87.9073,"USA",8,"US Midwest primary air cargo hub and intermodal connector"),
("AIR-LAX","Los Angeles International",["LAX"],"airport",["air","road"],33.9425,-118.4081,"USA",8,"US West Coast's primary air cargo and transpacific gateway"),
("AIR-ATLANTA","Hartsfield-Jackson Atlanta",["ATL","Atlanta Air"],"airport",["air","road"],33.6407,-84.4277,"USA",7,"US Southeast air cargo hub and connecting gateway"),
# === RAIL & INTERMODAL HUBS ===
("RAIL-CHICAGO","Chicago Intermodal Complex",["Chicago Rail","BNSF Logistics Park"],"rail_hub",["rail","road"],41.8781,-87.6298,"USA",9,"North America's largest rail interchange handling 25% of US freight rail"),
("RAIL-KANSASCITY","Kansas City Rail Hub",["KC Rail","KCS Hub"],"rail_hub",["rail","road"],39.0997,-94.5786,"USA",8,"Central US rail crossroads connecting four Class I railroads"),
("RAIL-DUISBURG","Duisburg Intermodal Terminal",["Duisburg","Duisport"],"rail_hub",["rail","road","sea"],51.4344,6.7623,"Germany",9,"World's largest inland port and China-Europe rail terminus"),
("RAIL-ZHENGZHOU","Zhengzhou International Hub",["Zhengzhou","Silk Road Terminal"],"rail_hub",["rail","road"],34.7466,113.6253,"China",8,"Primary China-Europe Railway Express origin terminal"),
("RAIL-CHENGDU","Chengdu International Rail Port",["Chengdu Rail","Qingbaijiang"],"rail_hub",["rail","road"],30.5728,104.0668,"China",8,"Western China Belt & Road rail gateway to Europe"),
("RAIL-DELHI","Delhi Tughlakabad ICD",["Delhi ICD","Tughlakabad"],"rail_hub",["rail","road"],28.5126,77.2771,"India",8,"India's largest inland container depot and North India rail hub"),
("RAIL-WARSAW","Warsaw Rail Terminal",["Warsaw","Malaszewicze"],"rail_hub",["rail","road"],52.2297,21.0122,"Poland",7,"EU-Asia rail gauge change point and BRI European gateway"),
# === DISTRIBUTION HUBS ===
("HUB-DALLAS","Alliance Texas Logistics Hub",["Dallas Hub","AllianceTexas","DFW Logistics"],"distribution_hub",["road","rail","air"],32.9715,-97.3190,"USA",8,"18,000-acre multimodal logistics hub with BNSF intermodal"),
("HUB-DUBAI","Dubai Logistics City",["DLC","JAFZA","Dubai South"],"distribution_hub",["road","air","sea"],24.8966,55.1500,"UAE",9,"World's largest airport-adjacent free zone and logistics cluster"),
("HUB-LAREDO","Laredo Border Crossing",["Laredo","US-Mexico Gateway"],"distribution_hub",["road","rail"],27.5036,-99.5076,"USA",8,"Busiest US-Mexico land port handling 40% of US-Mexico trade"),
("PORT-SEATTLE","Port of Seattle-Tacoma",["Seattle","Tacoma","NWSA"],"port",["sea","road","rail"],47.5801,-122.3450,"USA",8,"Pacific Northwest gateway and Alaska/Asia trade corridor"),
("PORT-OAKLAND","Port of Oakland",["Oakland"],"port",["sea","road","rail"],37.7956,-122.2789,"USA",7,"Northern California's primary container port"),
("AIR-COLOMBO","Bandaranaike International",["CMB","Colombo Air"],"airport",["air","road"],7.1808,79.8841,"Sri Lanka",7,"Indian Ocean air cargo transshipment and Sri Lanka gateway"),
("AIR-HYDERABAD","Rajiv Gandhi International",["HYD","Hyderabad Air"],"airport",["air","road"],17.2403,78.4294,"India",7,"India's pharma export hub and central logistics node"),
("RAIL-NHAVASHEVA","JNPT Rail Freight Terminal",["Nhava Sheva Rail","JNPT ICD"],"rail_hub",["rail","road"],18.9520,72.9510,"India",7,"Rail-port interface for India's largest container terminal"),
("HUB-NAGPUR","Nagpur MIHAN Hub",["Nagpur","MIHAN"],"distribution_hub",["road","rail","air"],21.0922,79.0472,"India",6,"India's geographic center multimodal logistics hub"),
("HUB-CALAIS","Calais Channel Tunnel Hub",["Calais","Eurotunnel","Coquelles"],"distribution_hub",["road","rail"],50.9281,1.8140,"France",7,"UK-Europe freight gateway handling 25% of cross-Channel trade"),
]

def build_hub(r):
    return {"id":r[0],"display_name":r[1],"aliases":r[2],"type":r[3],"modes":r[4],
            "lat":r[5],"lon":r[6],"country":r[7],"importance":r[8],"strategic_role":r[9]}

def validate(hubs):
    report = {"duplicate_ids":[],"duplicate_aliases":[],"missing_coordinates":[],"invalid_modes":[]}
    ids = set()
    aliases = {}
    valid_modes = {"sea","air","road","rail"}
    for h in hubs:
        if h["id"] in ids: report["duplicate_ids"].append(h["id"])
        ids.add(h["id"])
        for a in h["aliases"]:
            al = a.lower()
            if al in aliases: report["duplicate_aliases"].append(f"{a} -> [{aliases[al]}, {h['id']}]")
            aliases[al] = h["id"]
        if not h.get("lat") or not h.get("lon"): report["missing_coordinates"].append(h["id"])
        for m in h["modes"]:
            if m not in valid_modes: report["invalid_modes"].append(f"{h['id']}: {m}")
    report["total_hubs"] = len(hubs)
    report["total_issues"] = sum(len(v) for v in report.values() if isinstance(v,list))
    return report

if __name__ == "__main__":
    import json, os
    hubs = [build_hub(r) for r in RAW]
    report = validate(hubs)
    os.makedirs("backend/data", exist_ok=True)
    with open("backend/data/canonical_hubs.json","w") as f:
        json.dump(hubs, f, indent=2)
    with open("backend/data/validation_report.json","w") as f:
        json.dump(report, f, indent=2)
    print(f"Generated {report['total_hubs']} canonical hubs.")
    print(f"Validation issues: {report['total_issues']}")
    if report["duplicate_ids"]: print(f"  DUPLICATE IDS: {report['duplicate_ids']}")
    if report["duplicate_aliases"]: print(f"  DUPLICATE ALIASES: {report['duplicate_aliases']}")
    if report["missing_coordinates"]: print(f"  MISSING COORDS: {report['missing_coordinates']}")
    if report["invalid_modes"]: print(f"  INVALID MODES: {report['invalid_modes']}")
