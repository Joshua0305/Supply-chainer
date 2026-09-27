import json
import math

HUB_TEMPLATES = [
    # GUJARAT (50+ nodes)
    ("PORT-MUNDRA", "Port of Mundra", "port", 22.75, 69.7, 10, "India's largest private container port", "Mundra", "Gujarat"),
    ("PORT-HAZIRA", "Port of Hazira", "port", 21.1, 72.6, 8, "Deep-water port serving Surat industrial belt", "Hazira", "Gujarat"),
    ("PORT-KANDLA", "Deendayal Port (Kandla)", "port", 23.01, 70.22, 9, "Major cargo handling hub for West/North India", "Kandla", "Gujarat"),
    ("PORT-PIPAVAV", "Port of Pipavav", "port", 20.9, 71.5, 7, "Strategic container gateway in Saurashtra", "Pipavav", "Gujarat"),
    ("PORT-DAHEJ", "Port of Dahej", "port", 21.67, 72.58, 7, "Chemical and bulk cargo gateway", "Dahej", "Gujarat"),
    ("PORT-SIKKA", "Port of Sikka", "port", 22.43, 69.82, 7, "Petroleum and liquid cargo hub", "Jamnagar", "Gujarat"),
    ("PORT-OKHA", "Port of Okha", "port", 22.47, 69.07, 6, "Strategic gateway for North Saurashtra", "Okha", "Gujarat"),
    ("PORT-MAGDALLA", "Port of Magdalla", "port", 21.13, 72.72, 6, "Industrial port serving Surat", "Surat", "Gujarat"),
    ("PORT-VERAVAL", "Port of Veraval", "port", 20.91, 70.36, 5, "Secondary gateway for Saurashtra", "Veraval", "Gujarat"),
    ("PORT-BEDI", "Port of Bedi", "port", 22.5, 70.03, 5, "Bulk cargo terminal in Jamnagar", "Jamnagar", "Gujarat"),
    ("PORT-NAVBHAVNAGAR", "New Port Bhavnagar", "port", 21.75, 72.2, 5, "Regional bulk gateway", "Bhavnagar", "Gujarat"),
    ("PORT-MITHAPUR", "Port of Mithapur", "port", 22.42, 68.99, 5, "Chemical export gateway", "Mithapur", "Gujarat"),
    ("AIR-AHMEDABAD", "Ahmedabad Intl Airport", "airport", 23.07, 72.63, 8, "Primary air hub for Gujarat", "Ahmedabad", "Gujarat"),
    ("AIR-SURAT", "Surat Air Cargo Terminal", "airport", 21.11, 72.74, 7, "Export gateway for gems and textiles", "Surat", "Gujarat"),
    ("AIR-VADODARA", "Vadodara Cargo Hub", "airport", 22.33, 73.22, 6, "Logistics node for Central Gujarat", "Vadodara", "Gujarat"),
    ("AIR-RAJKOT", "Rajkot Cargo Hub", "airport", 22.31, 70.78, 6, "Air gateway for Saurashtra engineering belt", "Rajkot", "Gujarat"),
    ("AIR-BHAVNAGAR", "Bhavnagar Air Cargo", "airport", 21.75, 72.19, 5, "Regional air link for Saurashtra", "Bhavnagar", "Gujarat"),
    ("AIR-JAMNAGAR", "Jamnagar Air Base/Cargo", "airport", 22.48, 70.01, 5, "Strategic air gateway for Jamnagar industrial belt", "Jamnagar", "Gujarat"),
    ("AIR-BHUJ", "Bhuj Cargo Hub", "airport", 23.28, 69.67, 5, "Air link for Kutch logistics corridor", "Bhuj", "Gujarat"),
    ("RAIL-AHMEDABAD", "Ahmedabad Freight Terminal", "rail_terminal", 23.03, 72.58, 8, "Western DFC junction", "Ahmedabad", "Gujarat"),
    ("RAIL-VADODARA", "Vadodara Rail Junction", "rail_terminal", 22.31, 73.18, 7, "Critical junction on Mumbai-Delhi line", "Vadodara", "Gujarat"),
    ("RAIL-SURAT", "Surat Freight Junction", "rail_terminal", 21.2, 72.83, 7, "Major textile and diamond rail gateway", "Surat", "Gujarat"),
    ("RAIL-RAJKOT", "Rajkot Rail Hub", "rail_terminal", 22.3, 70.81, 6, "Freight node for Saurashtra region", "Rajkot", "Gujarat"),
    ("RAIL-GANDHIDHAM", "Gandhidham Rail Hub", "rail_terminal", 23.08, 70.13, 8, "Strategic rail junction serving Mundra and Kandla", "Gandhidham", "Gujarat"),
    ("RAIL-BHARUCH", "Bharuch Rail Junction", "rail_terminal", 21.71, 72.99, 6, "Critical freight junction for chemical belt", "Bharuch", "Gujarat"),
    ("DC-SANAND", "Sanand Industrial Cluster", "distribution_hub", 22.99, 72.38, 7, "Automotive manufacturing zone", "Sanand", "Gujarat"),
    ("DC-VAPI", "Vapi Industrial Belt", "distribution_hub", 20.37, 72.91, 7, "Chemical and pharma manufacturing cluster", "Vapi", "Gujarat"),
    ("DC-MORBI", "Morbi Ceramic Cluster", "distribution_hub", 22.82, 70.83, 7, "World's largest ceramic manufacturing hub", "Morbi", "Gujarat"),
    ("DC-JAMNAGAR", "Jamnagar Petrochemical Belt", "distribution_hub", 22.47, 70.06, 9, "World's largest refining hub", "Jamnagar", "Gujarat"),
    ("DC-BHARUCH", "Bharuch Industrial SEZ", "distribution_hub", 21.71, 72.99, 7, "Major chemical and fertilizer hub", "Bharuch", "Gujarat"),
    ("DC-ANKLESHWAR", "Ankleshwar Chemical Zone", "distribution_hub", 21.62, 73.0, 7, "Asia's largest chemical industrial estate", "Ankleshwar", "Gujarat"),
    ("DC-HAZIRA", "Hazira Industrial Area", "distribution_hub", 21.1, 72.65, 8, "Massive steel and manufacturing cluster", "Hazira", "Gujarat"),
    ("DC-KADI", "Kadi Industrial Belt", "distribution_hub", 23.3, 72.33, 6, "Manufacturing hub for North Gujarat", "Kadi", "Gujarat"),
    ("DC-HALOL", "Halol Manufacturing Hub", "distribution_hub", 22.5, 73.47, 6, "Automotive and general engineering cluster", "Halol", "Gujarat"),

    # MAHARASHTRA (40+ nodes)
    ("AIR-PUNE", "Pune Air Cargo Hub", "airport", 18.58, 73.92, 8, "Export gateway for auto/engineering", "Pune", "Maharashtra"),
    ("AIR-NAGPUR", "Nagpur MIHAN Cargo Hub", "airport", 21.09, 79.05, 8, "Strategic multi-modal hub", "Nagpur", "Maharashtra"),
    ("AIR-AURANGABAD", "Aurangabad Air Hub", "airport", 19.86, 75.40, 6, "Logistics node for DMIC corridor", "Aurangabad", "Maharashtra"),
    ("AIR-NASHIK", "Nashik Air Cargo Terminal", "airport", 20.12, 73.91, 6, "Air gateway for Nashik industrial belt", "Nashik", "Maharashtra"),
    ("PORT-RATNAGIRI", "Port of Ratnagiri", "port", 17.0, 73.28, 6, "Strategic coastal shipping hub", "Ratnagiri", "Maharashtra"),
    ("PORT-DHARAMTAR", "Port of Dharamtar", "port", 18.82, 73.03, 6, "Bulk cargo gateway near Mumbai", "Dharamtar", "Maharashtra"),
    ("PORT-JAIGAD", "Port of Jaigad", "port", 17.3, 73.2, 7, "Deep-water private port for Central Maharashtra", "Jaigad", "Maharashtra"),
    ("RAIL-PUNE", "Pune Logistics Terminal", "rail_terminal", 18.52, 73.85, 7, "Intermodal hub for Western Maharashtra", "Pune", "Maharashtra"),
    ("RAIL-NAGPUR", "Nagpur Freight Junction", "rail_terminal", 21.15, 79.08, 8, "North-South/East-West rail crossing", "Nagpur", "Maharashtra"),
    ("RAIL-BHUSAWAL", "Bhusawal Rail Junction", "rail_terminal", 21.05, 75.78, 7, "Major freight consolidation point", "Bhusawal", "Maharashtra"),
    ("RAIL-SOLAPUR", "Solapur Freight Terminal", "rail_terminal", 17.66, 75.9, 6, "Logistics hub for textiles and sugar", "Solapur", "Maharashtra"),
    ("RAIL-NASHIK", "Nashik Freight Hub", "rail_terminal", 20.0, 73.8, 7, "Rail gateway for Northern Maharashtra industrial belt", "Nashik", "Maharashtra"),
    ("RAIL-KALYAN", "Kalyan Rail Junction", "rail_terminal", 19.24, 73.13, 8, "Critical rail gateway for the Mumbai Metropolitan Region", "Kalyan", "Maharashtra"),
    ("DC-CHAKAN", "Chakan Manufacturing Zone", "distribution_hub", 18.75, 73.85, 8, "Automotive manufacturing heart", "Chakan", "Maharashtra"),
    ("DC-BHIWANDI", "Bhiwandi Warehousing Belt", "distribution_hub", 19.29, 73.06, 9, "India's premier logistics cluster", "Bhiwandi", "Maharashtra"),
    ("DC-TALOJA", "Taloja Industrial Estate", "distribution_hub", 19.06, 73.12, 7, "Chemical and engineering manufacturing hub", "Navi Mumbai", "Maharashtra"),
    ("DC-BUTIBORI", "Butibori Industrial Hub", "distribution_hub", 20.92, 78.94, 7, "Textile and chemical cluster near Nagpur", "Nagpur", "Maharashtra"),
    ("DC-AURANGABAD", "Aurangabad Industrial City", "distribution_hub", 19.92, 75.47, 7, "Strategic node on DMIC corridor", "Aurangabad", "Maharashtra"),
    ("DC-NASHIK", "Satpur-Ambad Industrial Hub", "distribution_hub", 19.95, 73.7, 7, "Engineering and auto manufacturing hub", "Nashik", "Maharashtra"),
    ("DC-HINJEWADI", "Hinjewadi Tech-Logistics Hub", "distribution_hub", 18.59, 73.73, 7, "Technology and high-value manufacturing cluster", "Pune", "Maharashtra"),

    # TAMIL NADU & SOUTH (60+ nodes)
    ("PORT-ENNORE", "Kamarajar Port (Ennore)", "port", 13.25, 80.34, 8, "Auto export and coal gateway", "Chennai", "Tamil Nadu"),
    ("PORT-KATTUPALLI", "Port of Kattupalli", "port", 13.31, 80.35, 7, "Container gateway for North Chennai", "Chennai", "Tamil Nadu"),
    ("PORT-TUTICORIN", "V.O.C. Port (Tuticorin)", "port", 8.75, 78.19, 8, "Strategic gateway for Southern TN", "Tuticorin", "Tamil Nadu"),
    ("PORT-NEWMANGALORE", "New Mangalore Port", "port", 12.92, 74.82, 7, "Major petroleum/bulk gateway", "Mangalore", "Karnataka"),
    ("PORT-KARWAR", "Port of Karwar", "port", 14.81, 74.12, 6, "Strategic maritime hub for North Karnataka", "Karwar", "Karnataka"),
    ("PORT-VISAKHAPATNAM", "Port of Visakhapatnam", "port", 17.69, 83.28, 9, "Deep-water mineral and bulk gateway", "Vizag", "Andhra Pradesh"),
    ("PORT-KRISHNAPATNAM", "Port of Krishnapatnam", "port", 14.25, 80.12, 8, "Major private gateway for Andhra", "Nellore", "Andhra Pradesh"),
    ("PORT-GANGAVARAM", "Port of Gangavaram", "port", 17.62, 83.23, 7, "Strategic industrial port for East Coast", "Vizag", "Andhra Pradesh"),
    ("AIR-HYDERABAD", "GMR Hyderabad Air Cargo", "airport", 17.24, 78.43, 9, "Pharma-capital of India", "Hyderabad", "Telangana"),
    ("AIR-BENGALURU", "KIA Bengaluru Cargo Hub", "airport", 13.20, 77.71, 9, "Electronics and tech cargo gateway", "Bengaluru", "Karnataka"),
    ("AIR-COIMBATORE", "Coimbatore Cargo Terminal", "airport", 11.03, 77.04, 7, "Export hub for engineering/textiles", "Coimbatore", "Tamil Nadu"),
    ("AIR-MADURAI", "Madurai Air Cargo Hub", "airport", 9.83, 78.09, 6, "Logistics gateway for Southern TN", "Madurai", "Tamil Nadu"),
    ("AIR-TRICHY", "Tiruchirappalli Cargo Hub", "airport", 10.76, 78.71, 6, "Air gateway for Delta industrial belt", "Trichy", "Tamil Nadu"),
    ("AIR-VIZAG", "Visakhapatnam Air Cargo", "airport", 17.72, 83.22, 7, "Strategic gateway for East Coast pharma", "Vizag", "Andhra Pradesh"),
    ("AIR-VIJAYAWADA", "Vijayawada Air Hub", "airport", 16.53, 80.79, 6, "Regional air link for Andhra industrial belt", "Vijayawada", "Andhra Pradesh"),
    ("AIR-MANGALORE", "Mangalore Air Cargo Hub", "airport", 12.96, 74.89, 6, "Coastal air gateway for Karnataka", "Mangalore", "Karnataka"),
    ("RAIL-VIJAYAWADA", "Vijayawada Rail Junction", "rail_terminal", 16.51, 80.62, 8, "Critical North-South rail gateway", "Vijayawada", "Andhra Pradesh"),
    ("RAIL-BENGALURU", "Bengaluru Logistics Terminal", "rail_terminal", 12.97, 77.59, 8, "Tech-logistics rail gateway", "Bengaluru", "Karnataka"),
    ("RAIL-HYDERABAD", "Hyderabad Freight Terminal", "rail_terminal", 17.38, 78.48, 8, "South-Central rail logistics hub", "Hyderabad", "Telangana"),
    ("RAIL-SALEM", "Salem Rail Junction", "rail_terminal", 11.66, 78.11, 7, "Critical steel and mineral rail gateway", "Salem", "Tamil Nadu"),
    ("RAIL-HUBBALLI", "Hubballi Rail Junction", "rail_terminal", 15.34, 75.14, 7, "Primary junction for North Karnataka", "Hubballi", "Karnataka"),
    ("RAIL-ARAKKONAM", "Arakkonam Rail Junction", "rail_terminal", 13.08, 79.66, 7, "Critical rail gateway connecting Chennai to West/North", "Arakkonam", "Tamil Nadu"),
    ("DC-SRIPERUMBUDUR", "Sriperumbudur Electronics Belt", "distribution_hub", 12.98, 79.95, 8, "Electronics/Auto manufacturing capital", "Chennai", "Tamil Nadu"),
    ("DC-HOSUR", "Hosur Industrial Belt", "distribution_hub", 12.74, 77.82, 7, "Precision engineering/Auto cluster", "Hosur", "Tamil Nadu"),
    ("DC-ORAGADAM", "Oragadam Auto Cluster", "distribution_hub", 12.83, 79.97, 8, "South Asia's largest auto manufacturing hub", "Chennai", "Tamil Nadu"),
    ("DC-SRICITY", "Sri City Integrated Hub", "distribution_hub", 13.55, 80.03, 8, "Global manufacturing hub for electronics", "Nellore", "Andhra Pradesh"),
    ("DC-HYDERABAD", "Hyderabad Pharma Cluster", "distribution_hub", 17.38, 78.48, 8, "Pharma manufacturing and R&D hub", "Hyderabad", "Telangana"),
    ("DC-BOMMASANDRA", "Bommasandra Industrial Zone", "distribution_hub", 12.81, 77.69, 7, "Precision and medical tech cluster", "Bengaluru", "Karnataka"),
    ("DC-PEENYA", "Peenya Industrial Belt", "distribution_hub", 13.03, 77.51, 7, "Major engineering and aerospace cluster", "Bengaluru", "Karnataka"),
    ("DC-BELAGAVI", "Belagavi Aerospace Hub", "distribution_hub", 15.85, 74.5, 6, "Precision machining and aerospace cluster", "Belagavi", "Karnataka"),
    ("DC-ORAGADAM-2", "Daimler-Renault Industrial Zone", "distribution_hub", 12.85, 79.98, 7, "Dedicated automotive export cluster", "Chennai", "Tamil Nadu"),
    ("DC-VALLAM", "Vallam Vadagal Manufacturing Hub", "distribution_hub", 12.9, 79.95, 7, "Emerging aerospace and auto manufacturing zone", "Chennai", "Tamil Nadu"),

    # NORTH INDIA (60+ nodes)
    ("AIR-LUCKNOW", "Lucknow Cargo Terminal", "airport", 26.76, 80.89, 7, "Gateway for Central UP industrial belt", "Lucknow", "Uttar Pradesh"),
    ("AIR-JAIPUR", "Jaipur Air Cargo Hub", "airport", 26.82, 75.81, 7, "Gems and handicrafts export gateway", "Jaipur", "Rajasthan"),
    ("AIR-CHANDIGARH", "Chandigarh Intl Airport", "airport", 30.67, 76.79, 7, "Pharma gateway for Punjab/Haryana", "Chandigarh", "Chandigarh"),
    ("AIR-AMRITSAR", "Amritsar Air Cargo Hub", "airport", 31.7, 74.8, 6, "Export gateway for North Punjab", "Amritsar", "Punjab"),
    ("AIR-VARANASI", "Varanasi Air Cargo Hub", "airport", 25.45, 82.85, 6, "Air gateway for Eastern UP", "Varanasi", "Uttar Pradesh"),
    ("RAIL-KANPUR", "Kanpur Freight Hub", "rail_terminal", 26.45, 80.33, 8, "Major logistics node on EDFC", "Kanpur", "Uttar Pradesh"),
    ("RAIL-LUDHIANA", "Ludhiana Logistics Hub", "rail_terminal", 30.90, 75.86, 8, "Textile logistics capital of India", "Ludhiana", "Punjab"),
    ("RAIL-MUGHALSARAI", "DDU Rail Junction (Mughalsarai)", "rail_terminal", 25.27, 83.13, 10, "Busiest freight rail junction in India", "Mughalsarai", "Uttar Pradesh"),
    ("RAIL-AGRA", "Agra Freight Junction", "rail_terminal", 27.17, 78.0, 7, "Logistics hub for Western UP", "Agra", "Uttar Pradesh"),
    ("RAIL-KOTA", "Kota Rail Hub", "rail_terminal", 25.21, 75.86, 7, "Critical industrial junction for Rajasthan", "Kota", "Rajasthan"),
    ("RAIL-DADRI", "Dadri ICD Hub", "rail_terminal", 28.53, 77.55, 9, "Strategic inland container depot", "Dadri", "Uttar Pradesh"),
    ("RAIL-REWARI", "Rewari DFC Junction", "rail_terminal", 28.19, 76.62, 8, "Major crossing of Western DFC and trunk lines", "Rewari", "Haryana"),
    ("RAIL-LUCKNOW", "Lucknow Freight Junction", "rail_terminal", 26.85, 80.94, 7, "Primary rail gateway for Central UP", "Lucknow", "Uttar Pradesh"),
    ("DC-NOIDA", "Noida Electronics Hub", "distribution_hub", 28.53, 77.39, 8, "Global smartphone manufacturing hub", "Noida", "Uttar Pradesh"),
    ("DC-GURGAON", "Gurgaon Manufacturing Belt", "distribution_hub", 28.46, 77.03, 8, "Corporate and auto heart of North", "Gurgaon", "Haryana"),
    ("DC-MANESAR", "Manesar Industrial Cluster", "distribution_hub", 28.36, 76.94, 8, "Auto manufacturing and parts hub", "Manesar", "Haryana"),
    ("DC-BAWAL", "Bawal Industrial Area", "distribution_hub", 28.08, 76.58, 7, "Auto and electronics cluster", "Bawal", "Haryana"),
    ("DC-PANTNAGAR", "Pantnagar Industrial Hub", "distribution_hub", 29.02, 79.49, 6, "Auto and FMCG manufacturing center", "Pantnagar", "Uttarakhand"),
    ("DC-TAPUKARA", "Tapukara Industrial Hub", "distribution_hub", 28.12, 76.81, 7, "Automotive manufacturing cluster in Rajasthan", "Bhiwadi", "Rajasthan"),
    ("DC-NEEMRANA", "Neemrana Japanese Zone", "distribution_hub", 28.0, 76.38, 8, "Strategic manufacturing cluster for Japanese firms", "Neemrana", "Rajasthan"),
    ("DC-KUNDLI", "Kundli Industrial Zone", "distribution_hub", 28.87, 77.11, 7, "Major food processing and manufacturing hub", "Sonipat", "Haryana"),
    ("DC-GREATER-NOIDA", "Greater Noida Manufacturing Belt", "distribution_hub", 28.47, 77.5, 8, "Electronics and high-tech manufacturing capital of North India", "Noida", "Uttar Pradesh"),

    # EAST & CENTRAL (40 nodes)
    ("PORT-PARADIP", "Port of Paradip", "port", 20.27, 86.67, 9, "Major mineral and energy gateway", "Paradip", "Odisha"),
    ("PORT-DHAMRA", "Port of Dhamra", "port", 20.82, 86.91, 7, "Deep-water mineral gateway", "Dhamra", "Odisha"),
    ("PORT-HALDIA", "Port of Haldia", "port", 22.03, 88.06, 8, "Industrial and bulk gateway for WB", "Haldia", "West Bengal"),
    ("AIR-GUWAHATI", "Guwahati Cargo Gateway", "airport", 26.11, 91.59, 7, "NE India's primary air link", "Guwahati", "Assam"),
    ("AIR-INDORE", "Indore Intl Airport", "airport", 22.72, 75.80, 7, "Air hub for Central India pharma", "Indore", "Madhya Pradesh"),
    ("AIR-BHUBANESWAR", "Bhubaneswar Air Cargo Hub", "airport", 20.24, 85.81, 7, "Air gateway for Odisha manufacturing belt", "Bhubaneswar", "Odisha"),
    ("RAIL-ITARSI", "Itarsi Strategic Junction", "rail_terminal", 22.61, 77.76, 9, "India's most critical rail junction", "Itarsi", "Madhya Pradesh"),
    ("RAIL-BILASPUR", "Bilaspur Rail Terminal", "rail_terminal", 22.08, 82.15, 8, "Major coal and mineral rail hub", "Bilaspur", "Chhattisgarh"),
    ("RAIL-RAIPUR", "Raipur Freight Junction", "rail_terminal", 21.25, 81.63, 7, "Strategic mineral gateway for Central-East", "Raipur", "Chhattisgarh"),
    ("RAIL-KHARAGPUR", "Kharagpur Rail Hub", "rail_terminal", 22.33, 87.32, 8, "Major rail gateway for Eastern India", "Kharagpur", "West Bengal"),
    ("RAIL-JHARSUGUDA", "Jharsuguda Freight Junction", "rail_terminal", 21.85, 84.03, 7, "Rail hub for aluminium corridor", "Jharsuguda", "Odisha"),
    ("RAIL-ADRA", "Adra Rail Junction", "rail_terminal", 23.49, 86.67, 7, "Critical rail gateway for the coal and steel belt", "Adra", "West Bengal"),
    ("DC-PITHAMPUR", "Pithampur Auto Cluster", "distribution_hub", 22.61, 75.68, 7, "Auto and pharma SEZ", "Indore", "Madhya Pradesh"),
    ("DC-JAMSHEDPUR", "Jamshedpur Steel Hub", "distribution_hub", 22.8, 86.2, 8, "Steel manufacturing capital of India", "Jamshedpur", "Jharkhand"),
    ("DC-RAIPUR", "Raipur Logistics Zone", "distribution_hub", 21.27, 81.71, 7, "Transit hub for minerals and metals", "Raipur", "Chhattisgarh"),
    ("DC-DANKUNI", "Dankuni Logistics Hub", "distribution_hub", 22.68, 88.3, 8, "Primary warehousing and distribution center for Greater Kolkata", "Kolkata", "West Bengal"),

    # INTERNATIONAL (Expansion)
    ("AIR-DOHA", "Hamad Intl Cargo Terminal", "airport", 25.27, 51.61, 10, "Global relay hub for Middle East and Europe", "Doha", "Qatar"),
    ("AIR-HONGKONG", "Hong Kong Air Cargo Hub", "airport", 22.31, 113.93, 10, "Primary global gateway for East Asian manufacturing", "Hong Kong", "China"),
    ("AIR-DUBAI", "Dubai World Central", "airport", 24.89, 55.16, 10, "World's largest multi-modal logistics platform", "Dubai", "UAE"),
    ("PORT-COLOMBO", "Port of Colombo", "port", 6.95, 79.85, 9, "Critical transshipment hub for South Asia", "Colombo", "Sri Lanka"),
    ("PORT-SINGAPORE", "Port of Singapore", "port", 1.26, 103.83, 10, "Global maritime transshipment capital", "Singapore", "Singapore"),
]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

FINAL_NODES = []
for id, name, type, lat, lon, imp, role, city, region in HUB_TEMPLATES:
    modes = ["road"]
    if type == "port": modes.append("sea")
    if type == "airport": modes.append("air")
    if type == "rail_terminal": modes.append("rail")
    if type == "distribution_hub": modes.append("road")

    node = {
        "id": id, "display_name": name, "aliases": [name.split(" ")[0]], "type": type,
        "modes": list(set(modes)), "lat": lat, "lon": lon, "country": "India" if "AIR-DOHA" not in id and "AIR-HONGKONG" not in id and "AIR-DUBAI" not in id and "PORT-COLOMBO" not in id and "PORT-SINGAPORE" not in id else "International",
        "importance": imp, "strategic_role": role, "parent_city": city,
        "region": region, "connections": []
    }
    FINAL_NODES.append(node)

def add_conn(u_id, v_id, mode):
    for n in FINAL_NODES:
        if n["id"] == u_id:
            if not any(c["to"] == v_id for c in n["connections"]):
                n["connections"].append({"to": v_id, "mode": mode})
        if n["id"] == v_id:
            if not any(c["to"] == u_id for c in n["connections"]):
                n["connections"].append({"to": u_id, "mode": mode})

# COASTAL SHIPPING (SEA)
PORT_NODES = sorted([n for n in FINAL_NODES if n["type"] == "port"], key=lambda x: (x["lat"], x["lon"]))
for i in range(len(PORT_NODES)-1):
    add_conn(PORT_NODES[i]["id"], PORT_NODES[i+1]["id"], "sea")

# NATIONAL AIR TRUNK
AIR_NODES = [n["id"] for n in FINAL_NODES if n["type"] == "airport"]
MAJOR_AIR_HUBS = ["AIR-MUMBAI", "AIR-DELHI", "AIR-BENGALURU", "AIR-HYDERABAD", "AIR-CHENNAI", "AIR-DOHA", "AIR-HONGKONG", "AIR-DUBAI"]
for hub in MAJOR_AIR_HUBS:
    for target in AIR_NODES:
        if hub != target: add_conn(hub, target, "air")

# RAIL FREIGHT BACKBONE
RAIL_NODES = [n["id"] for n in FINAL_NODES if n["type"] == "rail_terminal"]
# Core DFC/Trunk
add_conn("RAIL-MUGHALSARAI", "RAIL-KANPUR", "rail")
add_conn("RAIL-MUGHALSARAI", "RAIL-VARANASI", "rail")
add_conn("RAIL-KANPUR", "RAIL-DADRI", "rail")
add_conn("RAIL-DADRI", "RAIL-DELHI", "rail")
add_conn("RAIL-ITARSI", "RAIL-AGRA", "rail")
add_conn("RAIL-ITARSI", "RAIL-NAGPUR", "rail")
add_conn("RAIL-ITARSI", "RAIL-AHMEDABAD", "rail")
add_conn("RAIL-ITARSI", "RAIL-BHOPAL", "rail")
add_conn("RAIL-NAGPUR", "RAIL-BILASPUR", "rail")
add_conn("RAIL-BILASPUR", "RAIL-RAIPUR", "rail")
add_conn("RAIL-RAIPUR", "RAIL-JHARSUGUDA", "rail")
add_conn("RAIL-JHARSUGUDA", "RAIL-SAMBALPUR", "rail")
add_conn("RAIL-VIJAYAWADA", "RAIL-HYDERABAD", "rail")
add_conn("RAIL-VIJAYAWADA", "RAIL-CHENNAI", "rail")
add_conn("RAIL-VIJAYAWADA", "RAIL-VISAKHAPATNAM", "rail")
add_conn("RAIL-KHARAGPUR", "RAIL-JHARSUGUDA", "rail")
add_conn("RAIL-REWARI", "RAIL-DADRI", "rail")
add_conn("RAIL-REWARI", "RAIL-AHMEDABAD", "rail")

# LOCAL ROAD INTERMODAL
for i, n1 in enumerate(FINAL_NODES):
    for n2 in FINAL_NODES[i+1:]:
        d = haversine(n1["lat"], n1["lon"], n2["lat"], n2["lon"])
        if d < 180:
            add_conn(n1["id"], n2["id"], "road")

# CONNECT TO BASE HUB MAPPING
BASE_HUBS = ["PORT-MUMBAI", "AIR-MUMBAI", "HUB-MUMBAI", "AIR-DELHI", "RAIL-DELHI", "PORT-CHENNAI", "AIR-COK", "PORT-KOCHI", "RAIL-KOCHI", "DC-KOCHI", "AIR-DOHA", "PORT-SINGAPORE", "PORT-COLOMBO"]
for bh in BASE_HUBS:
    bh_lat, bh_lon = 0, 0
    if "MUMBAI" in bh: bh_lat, bh_lon = 18.9, 72.8
    if "DELHI" in bh: bh_lat, bh_lon = 28.6, 77.2
    if "CHENNAI" in bh: bh_lat, bh_lon = 13.0, 80.2
    if "KOCHI" in bh: bh_lat, bh_lon = 9.9, 76.2
    if "DOHA" in bh: bh_lat, bh_lon = 25.3, 51.5
    if "SINGAPORE" in bh: bh_lat, bh_lon = 1.3, 103.8
    if "COLOMBO" in bh: bh_lat, bh_lon = 6.9, 79.8
    
    for n in FINAL_NODES:
        d = haversine(bh_lat, bh_lon, n["lat"], n["lon"])
        if d < 300:
            add_conn(bh, n["id"], "road")

with open("scratch/expanded_indian_hubs.json", "w") as f:
    json.dump(FINAL_NODES, f, indent=2)

print(f"Generated {len(FINAL_NODES)} strategic Indian hubs with bidirectional corridors.")
