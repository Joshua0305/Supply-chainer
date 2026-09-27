#!/usr/bin/env python3
"""Part 2: Hubs 101-200. Append to existing canonical_hubs.json."""
import json, os

RAW2 = [
# === SOUTH AMERICA EXPANSION ===
("PORT-BUENOSAIRES","Port of Buenos Aires",["Buenos Aires","Dock Sud"],"port",["sea","road","rail"],-34.6118,-58.3656,"Argentina",7,"Argentina's primary container port and Mercosur trade gateway"),
("PORT-CALLAO","Port of Callao",["Callao","Lima Port"],"port",["sea","road"],-12.0464,-77.1185,"Peru",7,"Peru's largest port handling 75% of national maritime trade"),
("PORT-CARTAGENA","Port of Cartagena",["Cartagena Colombia"],"port",["sea","road"],10.3997,-75.5144,"Colombia",8,"Caribbean transshipment hub and Colombia's primary container port"),
("PORT-VALPARAISO","Port of Valparaiso",["Valparaiso","San Antonio"],"port",["sea","road","rail"],-33.0472,-71.6127,"Chile",7,"Chile's primary container port and Pacific South America gateway"),
("PORT-ITAJAI","Port of Itajai-Navegantes",["Itajai","Navegantes"],"port",["sea","road"],-26.9022,-48.6653,"Brazil",7,"Brazil's third largest container port in Santa Catarina"),
("PORT-MONTEVIDEO","Port of Montevideo",["Montevideo"],"port",["sea","road"],-34.9055,-56.2120,"Uruguay",6,"Rio de la Plata gateway and Mercosur feeder port"),
("PORT-GUAYAQUIL","Port of Guayaquil",["Guayaquil","Contecon"],"port",["sea","road"],-2.2119,-79.9070,"Ecuador",6,"Ecuador's primary port and banana/shrimp export gateway"),
("AIR-SAOPAULO","Guarulhos International",["GRU","Sao Paulo Air"],"airport",["air","road"],-23.4356,-46.4731,"Brazil",8,"Latin America's largest air cargo hub"),
("AIR-BOGOTA","El Dorado International",["BOG","Bogota Air"],"airport",["air","road"],4.7016,-74.1469,"Colombia",7,"Andean region primary air cargo hub and flower export gateway"),
("AIR-SANTIAGO","Arturo Merino Benitez Intl",["SCL","Santiago Air"],"airport",["air","road"],-33.3930,-70.7858,"Chile",7,"Chile's air cargo gateway for high-value Pacific trade"),
("AIR-MEXICO","Mexico City International",["MEX","Benito Juarez"],"airport",["air","road"],19.4363,-99.0721,"Mexico",8,"Latin America's second largest air cargo airport"),
# === AFRICA EXPANSION ===
("PORT-LAGOS","Lagos Tin Can/Apapa Port",["Lagos Port","Apapa","Tin Can"],"port",["sea","road"],6.4389,3.3842,"Nigeria",8,"West Africa's largest port complex and Nigeria trade gateway"),
("PORT-ABIDJAN","Port of Abidjan",["Abidjan"],"port",["sea","road","rail"],5.2869,-3.9625,"Ivory Coast",7,"West Africa's second largest port and Sahel transit corridor"),
("PORT-DARESSALAAM","Port of Dar es Salaam",["Dar es Salaam"],"port",["sea","road","rail"],-6.8235,39.2695,"Tanzania",7,"East Africa's second gateway serving landlocked nations"),
("PORT-MAPUTO","Port of Maputo",["Maputo"],"port",["sea","road","rail"],-25.9653,32.5892,"Mozambique",6,"Southern Africa corridor port serving Eswatini and Zimbabwe"),
("PORT-CAPETOWN","Port of Cape Town",["Cape Town"],"port",["sea","road","rail"],-33.9141,18.4339,"South Africa",7,"Cape route alternative gateway and reefer cargo hub"),
("PORT-ALEXANDR","Port of Alexandria",["Alexandria","El Dekheila"],"port",["sea","road","rail"],31.1842,29.8623,"Egypt",7,"Egypt's primary Mediterranean container port"),
("PORT-LOME","Port of Lome",["Lome"],"port",["sea","road"],6.1319,1.2854,"Togo",6,"West Africa deep-water transshipment hub"),
("AIR-JOHANNESBURG","OR Tambo International",["JNB","Johannesburg Air"],"airport",["air","road"],-26.1367,28.2411,"South Africa",8,"Africa's busiest cargo airport and sub-Saharan air hub"),
("AIR-NAIROBI","Jomo Kenyatta International",["NBO","Nairobi Air"],"airport",["air","road"],-1.3192,36.9278,"Kenya",7,"East Africa's primary air cargo hub and flower export center"),
("AIR-ADDISABABA","Bole International Airport",["ADD","Addis Ababa Air"],"airport",["air","road"],8.9779,38.7993,"Ethiopia",7,"Ethiopian Cargo hub and Africa-to-world air freight gateway"),
("AIR-CAIRO","Cairo International Airport",["CAI","Cairo Air"],"airport",["air","road"],30.1219,31.4056,"Egypt",7,"North Africa's primary air cargo terminal"),
# === CENTRAL ASIA & RUSSIA ===
("RAIL-KHORGOS","Khorgos Gateway",["Khorgos","Altynkol"],"rail_hub",["rail","road"],44.2275,80.2700,"Kazakhstan",8,"China-Kazakhstan border crossing and BRI dry port mega-hub"),
("RAIL-MOSCOW","Moscow Freight Terminal",["Moscow Rail","Vorsino"],"rail_hub",["rail","road"],55.7558,37.6173,"Russia",8,"Russia's central rail freight hub and Trans-Siberian anchor"),
("RAIL-NOVOSIBIRSK","Novosibirsk Rail Terminal",["Novosibirsk","Kleshchikha"],"rail_hub",["rail","road"],55.0084,82.9357,"Russia",7,"Trans-Siberian Railway midpoint and Siberian distribution center"),
("PORT-VLADIVOSTOK","Port of Vladivostok",["Vladivostok"],"port",["sea","road","rail"],43.1056,131.8735,"Russia",7,"Russia's Pacific gateway and Trans-Siberian eastern terminus"),
("PORT-STPETERSBURG","Port of St. Petersburg",["St. Petersburg","Big Port"],"port",["sea","road","rail"],59.9343,30.3351,"Russia",7,"Russia's Baltic Sea primary container port"),
("RAIL-TASHKENT","Tashkent Freight Hub",["Tashkent"],"rail_hub",["rail","road"],41.2995,69.2401,"Uzbekistan",6,"Central Asia's rail crossroads and cotton/mineral export hub"),
("RAIL-ALMATY","Almaty Logistics Center",["Almaty"],"rail_hub",["rail","road"],43.2220,76.8512,"Kazakhstan",6,"Kazakhstan's commercial capital rail terminal"),
("AIR-BAKU","Heydar Aliyev International",["GYD","Baku Air"],"airport",["air","road"],40.4675,50.0467,"Azerbaijan",6,"Caspian region air cargo hub and East-West corridor node"),
# === EASTERN EUROPE ===
("PORT-CONSTANTA","Port of Constanta",["Constanta"],"port",["sea","road","rail"],44.1598,28.6348,"Romania",7,"Black Sea's largest port and Danube corridor gateway"),
("PORT-KOPER","Port of Koper",["Koper"],"port",["sea","road","rail"],45.5469,13.7248,"Slovenia",7,"Adriatic deep-water port serving Central European hinterland"),
("PORT-THESSALONIKI","Port of Thessaloniki",["Thessaloniki"],"port",["sea","road","rail"],40.6279,22.9522,"Greece",6,"Northern Greece gateway and Balkans corridor entry"),
("RAIL-BUDAPEST","Budapest Intermodal Terminal",["Budapest Rail","BILK"],"rail_hub",["rail","road"],47.4979,19.0402,"Hungary",7,"Central European rail crossroads on Rhine-Danube corridor"),
("HUB-PRAGUE","Prague Logistics Park",["Prague","CTPark"],"distribution_hub",["road","rail"],50.0755,14.4378,"Czech Republic",6,"Central European distribution hub for automotive and electronics"),
# === SOUTHEAST ASIA DEEP COVERAGE ===
("PORT-JAKARTA","Tanjung Priok Port",["Jakarta Port","Tanjung Priok"],"port",["sea","road"],-6.0989,106.8869,"Indonesia",8,"Indonesia's busiest port handling 50%+ of national container trade"),
("PORT-SURABAYA","Tanjung Perak Port",["Surabaya Port","Tanjung Perak"],"port",["sea","road"],-7.2000,112.7333,"Indonesia",7,"East Java's primary port and eastern Indonesia distribution hub"),
("PORT-MANILA","Port of Manila",["Manila","MICT","South Harbor"],"port",["sea","road"],14.5833,120.9500,"Philippines",7,"Philippines' primary container port complex"),
("PORT-HAIPHONG","Hai Phong Port",["Hai Phong","Lach Huyen"],"port",["sea","road","rail"],20.8449,106.6881,"Vietnam",7,"Northern Vietnam's deep-sea port serving Hanoi manufacturing"),
("PORT-YANGON","Myanmar International Terminal",["Yangon Port","Thilawa"],"port",["sea","road"],16.8661,96.1951,"Myanmar",6,"Myanmar's primary port and Thilawa SEZ gateway"),
("PORT-SIHANOUKVILLE","Port of Sihanoukville",["Sihanoukville"],"port",["sea","road"],10.6267,103.5113,"Cambodia",6,"Cambodia's sole deep-water port and garment export gateway"),
("AIR-BANGKOK","Suvarnabhumi Airport",["BKK","Bangkok Air"],"airport",["air","road"],13.6900,100.7501,"Thailand",8,"Southeast Asia's second largest cargo airport"),
("AIR-KUALALUMPUR","KL International Airport",["KUL","KLIA Cargo"],"airport",["air","road"],2.7456,101.7099,"Malaysia",7,"Malaysia's primary air cargo hub and regional e-commerce center"),
("AIR-HANOI","Noi Bai International",["HAN","Hanoi Air"],"airport",["air","road"],21.2187,105.8044,"Vietnam",7,"Northern Vietnam's air cargo gateway for electronics exports"),
("AIR-MANILA","Ninoy Aquino International",["MNL","Manila Air"],"airport",["air","road"],14.5086,121.0198,"Philippines",7,"Philippines primary air cargo terminal and semiconductor hub"),
# === AUSTRALIA / OCEANIA ===
("PORT-MELBOURNE","Port of Melbourne",["Melbourne Port"],"port",["sea","road","rail"],-37.8230,144.9133,"Australia",8,"Australia's largest container port handling 36% of national trade"),
("PORT-SYDNEY","Port Botany Sydney",["Sydney Port","Port Botany"],"port",["sea","road","rail"],-33.9600,151.2200,"Australia",7,"New South Wales primary container port and import gateway"),
("PORT-BRISBANE","Port of Brisbane",["Brisbane Port"],"port",["sea","road","rail"],-27.3820,153.1725,"Australia",7,"Queensland's primary port and Northern Australia gateway"),
("PORT-FREMANTLE","Fremantle Port",["Fremantle","Perth Port"],"port",["sea","road","rail"],-32.0569,115.7439,"Australia",7,"Western Australia's primary container port for Indian Ocean trade"),
("PORT-TAURANGA","Port of Tauranga",["Tauranga"],"port",["sea","road","rail"],-37.6878,176.1651,"New Zealand",7,"New Zealand's largest export port by TEU volume"),
("AIR-SYDNEY","Sydney Kingsford Smith",["SYD","Sydney Air"],"airport",["air","road"],-33.9399,151.1753,"Australia",8,"Oceania's largest air cargo hub"),
("AIR-MELBOURNE","Melbourne Tullamarine",["MEL","Melbourne Air"],"airport",["air","road"],-37.6690,144.8410,"Australia",7,"Australia's second air cargo hub and pharma import center"),
("AIR-AUCKLAND","Auckland International",["AKL","Auckland Air"],"airport",["air","road"],-37.0082,174.7850,"New Zealand",6,"New Zealand's primary air cargo and perishable export gateway"),
# === ADDITIONAL STRATEGIC PORTS (ASIA & MIDDLE EAST) ===
("PORT-HAMAD","Hamad Port",["Hamad","Doha Port"],"port",["sea","road"],25.0103,51.6206,"Qatar",7,"Qatar's mega-port replacing Doha Port for container and bulk operations"),
("PORT-SOHAR","Port of Sohar",["Sohar"],"port",["sea","road"],24.3440,56.7280,"Oman",7,"Oman's industrial port on Strait of Hormuz approach"),
("PORT-BANDARABBAS","Bandar Abbas Port",["Bandar Abbas","Shahid Rajaee"],"port",["sea","road","rail"],27.1833,56.2833,"Iran",7,"Iran's largest container port on Strait of Hormuz"),
("PORT-KARACHI","Port of Karachi",["Karachi","KICT"],"port",["sea","road","rail"],24.8465,66.9791,"Pakistan",8,"Pakistan's primary port handling 60% of national trade"),
("PORT-CHITTAGONG","Port of Chittagong",["Chittagong","Chattogram"],"port",["sea","road"],22.2949,91.7851,"Bangladesh",7,"Bangladesh's main port handling 92% of national import-export"),
("PORT-DALIAN","Port of Dalian",["Dalian"],"port",["sea","road","rail"],38.9140,121.5867,"China",8,"Northeast China gateway and bulk commodity import terminal"),
("PORT-XIAMEN","Port of Xiamen",["Xiamen","Haicang"],"port",["sea","road","rail"],24.4798,118.0894,"China",8,"Fujian province container hub and Taiwan Strait trade node"),
# === ADDITIONAL EUROPEAN HUBS ===
("PORT-BREMERHAVEN","Port of Bremerhaven",["Bremerhaven","Bremen"],"port",["sea","road","rail"],53.5396,8.5809,"Germany",8,"Europe's fourth largest container port and auto logistics hub"),
("PORT-BARCELONA","Port of Barcelona",["Barcelona"],"port",["sea","road","rail"],41.3569,2.1686,"Spain",7,"Western Mediterranean container and cruise logistics hub"),
("PORT-GENOA","Port of Genoa",["Genoa","Genova"],"port",["sea","road","rail"],44.4056,8.9463,"Italy",7,"Italy's largest port and Southern Europe distribution gateway"),
("PORT-ALGECIRAS","Port of Algeciras",["Algeciras"],"port",["sea","road"],36.1281,-5.4437,"Spain",8,"Mediterranean transshipment hub at Strait of Gibraltar"),
("PORT-GIOIA","Gioia Tauro Port",["Gioia Tauro"],"port",["sea","road","rail"],38.4273,15.8939,"Italy",7,"Central Mediterranean transshipment hub for Africa-Europe trade"),
("AIR-AMSTERDAM","Amsterdam Airport Cargo",["AMS Cargo"],"airport",["air","road","rail"],52.3086,4.7639,"Netherlands",8,"European pharma and high-value air freight center"),
("HUB-VENLO","Venlo Logistics Corridor",["Venlo","Fresh Park"],"distribution_hub",["road","rail"],51.3704,6.1724,"Netherlands",6,"Europe's largest fresh produce logistics hub and crossdock center"),
# === ADDITIONAL RAIL/INLAND HUBS ===
("RAIL-XIAN","Xi'an International Port",["Xi'an Rail","Chang'an"],"rail_hub",["rail","road"],34.2630,108.9424,"China",8,"Belt & Road inland port and China-Europe Express major terminal"),
("RAIL-URUMQI","Urumqi Rail Terminal",["Urumqi"],"rail_hub",["rail","road"],43.8256,87.6168,"China",7,"Western China rail gateway to Central Asia and Europe"),
("RAIL-HAMBURG","Hamburg Rail Hub",["Hamburg Maschen"],"rail_hub",["rail","road"],53.4598,9.9610,"Germany",8,"Europe's largest rail marshalling yard"),
("RAIL-LOSANGELES","LA Intermodal Complex",["LA Rail","ICTF"],"rail_hub",["rail","road"],33.8091,-118.2449,"USA",8,"US West Coast's largest rail-port intermodal facility"),
("RAIL-CHENNAI","Chennai ICD Complex",["Chennai Rail","Tondiarpet"],"rail_hub",["rail","road"],13.1368,80.2908,"India",7,"South India's primary inland container depot cluster"),
("RAIL-MUNDRA","Mundra Rail Corridor",["Mundra Rail","GPPL"],"rail_hub",["rail","road"],22.7500,69.7000,"India",7,"Dedicated freight corridor rail head for Mundra port hinterland"),
("HUB-MEMPHIS","Memphis Logistics Hub",["Memphis Freight","Memphis TN"],"distribution_hub",["road","rail","air"],35.1495,-90.0490,"USA",8,"Intermodal crossroads co-located with FedEx SuperHub"),
("HUB-LOUISVILLE","Louisville Logistics Park",["Louisville KY"],"distribution_hub",["road","rail","air"],38.2527,-85.7585,"USA",7,"UPS Worldport adjacent distribution mega-cluster"),
("HUB-ROTTERDAM","Rotterdam Distripark",["Distripark","Maasvlakte DC"],"distribution_hub",["road","rail","sea"],51.9500,4.0300,"Netherlands",8,"Europe's largest port-adjacent distribution and value-added zone"),
# === LATIN AMERICA FREIGHT CORRIDORS ===
("PORT-LAZAROCARDENAS","Port of Lazaro Cardenas",["Lazaro Cardenas"],"port",["sea","road","rail"],17.9356,-102.1820,"Mexico",7,"Mexico's Pacific deep-water port and Asia trade gateway"),
("PORT-PARANAGUA","Port of Paranagua",["Paranagua"],"port",["sea","road","rail"],-25.5161,-48.5225,"Brazil",7,"Brazil's primary grain and soybean export port"),
("PORT-BALBOA","Port of Balboa",["Balboa","Panama Pacific"],"port",["sea","road"],8.9500,-79.5667,"Panama",7,"Pacific-side Panama Canal container terminal"),
("AIR-LIMA","Jorge Chavez International",["LIM","Lima Air"],"airport",["air","road"],-12.0219,-77.1143,"Peru",7,"Andean region air cargo hub and perishable export center"),
("AIR-PANAMA","Tocumen International",["PTY","Panama Air"],"airport",["air","road"],9.0714,-79.3835,"Panama",7,"Americas air transit hub and Copa Cargo gateway"),
("HUB-MONTERREY","Monterrey Industrial Hub",["Monterrey","Nuevo Leon"],"distribution_hub",["road","rail"],25.6866,-100.3161,"Mexico",7,"Mexico's northern industrial corridor and nearshoring hub"),
]

def build_hub(r):
    return {"id":r[0],"display_name":r[1],"aliases":r[2],"type":r[3],"modes":r[4],
            "lat":r[5],"lon":r[6],"country":r[7],"importance":r[8],"strategic_role":r[9]}

if __name__ == "__main__":
    # Load existing Part 1
    with open("backend/data/canonical_hubs.json","r") as f:
        existing = json.load(f)
    existing_ids = {h["id"] for h in existing}
    existing_aliases = set()
    for h in existing:
        for a in h["aliases"]:
            existing_aliases.add(a.lower())

    new_hubs = [build_hub(r) for r in RAW2]
    
    # Validate against Part 1
    dupes = [h["id"] for h in new_hubs if h["id"] in existing_ids]
    alias_collisions = []
    for h in new_hubs:
        for a in h["aliases"]:
            if a.lower() in existing_aliases:
                alias_collisions.append(f"{a} (in {h['id']})")
    
    if dupes:
        print(f"FATAL: Duplicate IDs with Part 1: {dupes}")
    if alias_collisions:
        print(f"WARNING: Alias collisions with Part 1: {alias_collisions}")
    
    # Merge and write
    merged = existing + new_hubs
    with open("backend/data/canonical_hubs.json","w") as f:
        json.dump(merged, f, indent=2)
    
    # Validation
    report = {"total_hubs": len(merged), "part2_added": len(new_hubs),
              "duplicate_ids_with_part1": dupes, "alias_collisions": alias_collisions}
    with open("backend/data/validation_report.json","w") as f:
        json.dump(report, f, indent=2)
    
    print(f"Part 2 merged: {len(new_hubs)} new hubs. Total: {len(merged)}")
    print(f"Cross-part duplicate IDs: {len(dupes)}")
    print(f"Cross-part alias collisions: {len(alias_collisions)}")
