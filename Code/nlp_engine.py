from sentence_transformers import SentenceTransformer, util
import torch
import re

class SupplyChainNLP:
    def __init__(self):
        print("Loading Advanced Contrastive NLP Brain (all-MiniLM-L6-v2)...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        self.disaster_anchors = [
            "Catastrophic hurricane, typhoon, and severe weather destroys port.",
            "Massive earthquake and tsunami devastates coastal logistics hubs.",
            "Massive global worker strike and union protest shuts down logistics network.",
            "Massive bridge collapse and highway destruction severs supply chain artery.",
            "Cyberattack shuts down global port operating systems and tracking.",
            "Military blockade, war, and geopolitical conflict closes major maritime strait.",
            "Armed pirates hijack commercial vessel and hold crew hostage.",
            "Government embargo, bombs, and trade war halts international freight."
        ]
        
        self.safe_anchors = [
            "Normal traffic, clear weather, sunny skies, and smooth operations.",
            "Routine delivery on time, no delays, safe and secure transport.",
            "Positive economic growth, peaceful conditions, business as usual.",
            "Traffic is flowing normally, roads are completely empty and clear."
        ]
        
        self.disaster_embeddings = self.model.encode(self.disaster_anchors, convert_to_tensor=True)
        self.safe_embeddings = self.model.encode(self.safe_anchors, convert_to_tensor=True)
        print("Contrastive NLP Matrix Ready!")

    def chunk_text(self, text: str) -> list:
        sentences = re.split(r'(?<=[.!?]) +', text)
        return [s.strip() for s in sentences if len(s.split()) > 3]

    def generate_severity_score(self, news_text: str) -> float:
        chunks = self.chunk_text(news_text)
        if not chunks:
            return 0.0

        chunk_embeddings = self.model.encode(chunks, convert_to_tensor=True)
        
        disaster_scores = util.cos_sim(chunk_embeddings, self.disaster_embeddings)
        safe_scores = util.cos_sim(chunk_embeddings, self.safe_embeddings)
        
        max_final_threat = 0.0
        
        for i in range(len(chunks)):
            best_disaster = torch.max(disaster_scores[i]).item()
            best_safe = torch.max(safe_scores[i]).item()
            
            margin = best_disaster - best_safe
            
            if margin > max_final_threat:
                max_final_threat = margin
                
        if max_final_threat <= 0.08:
            return 0.0
            
        calibration_multiplier = 3.5 
        final_score = min(1.0, max_final_threat * calibration_multiplier)
        
        return final_score
    def calculate_relevance(self, news_text: str, mode: str, origin: str, destination: str) -> float:
        text_lower = news_text.lower()
        
        sea_keywords = ['sea', 'ocean', 'ship', 'port', 'naval', 'canal', 'strait', 'maritime', 'pirate', 'vessel']
        air_keywords = ['air', 'flight', 'airport', 'plane', 'aviation', 'sky', 'airspace']
        road_keywords = ['road', 'highway', 'truck', 'traffic', 'bridge', 'street', 'warehouse', 'delivery', 'van', 'bike']
        
        mode_str = str(mode).lower()
        if mode_str in ['air', 'aeroplane', 'flight']:
            if any(word in text_lower for word in sea_keywords + road_keywords) and not any(word in text_lower for word in air_keywords):
                return 0.0 
                
        elif mode_str in ['sea', 'ocean', 'ship', 'freight']:
            if any(word in text_lower for word in air_keywords + road_keywords) and not any(word in text_lower for word in sea_keywords):
                return 0.0 
                
        elif mode_str in ['truck', 'bike', 'ev van', 'van', 'scooter', 'ev bike']:
            if any(word in text_lower for word in sea_keywords + air_keywords) and not any(word in text_lower for word in road_keywords):
                return 0.0 

        # --- SPATIAL RELEVANCE ---
        global_keywords = ['global', 'world', 'international', 'pandemic', 'war']
        if any(word in text_lower for word in global_keywords):
            return 1.0
            
        if str(origin).lower() in text_lower or str(destination).lower() in text_lower:
            return 1.0
          
        return 0.2

if __name__ == "__main__":
    nlp = SupplyChainNLP()
    
    print("Test cases:")

    test_cases = [
        (
            "Test 1: Pure Safe Baseline", 
            "The delivery truck is on its way. Weather is clear, skies are sunny, and roads are completely empty."
        ),
        (
            "Test 2: Minor Nuisance", 
            "There is slight traffic near the downtown area due to a local food festival. Drivers might be delayed by ten minutes."
        ),
        (
            "Test 3: The Diluted Black Swan", 
            "The global economy is seeing massive growth. Stock markets are hitting all-time highs. Tech companies are thriving. However, a massive bomb destroyed the Suez Canal. Sports teams played well today, and agriculture is booming."
        ),
        (
            "Test 4: Unseen Semantic Threat", 
            "Armed pirates have hijacked a major commercial cargo vessel off the coast of Somalia and are holding the crew hostage."
        ),
        (
            "Test 5: Catastrophic Infrastructure Failure", 
            "A 9.0 magnitude earthquake has completely leveled the primary dispatch warehouse and shattered all connecting suspension bridges in the region."
        )
    ]

    for name, text in test_cases:
        score = nlp.generate_severity_score(text)
        print(f"--- {name} ---")
        print(f"Report: \"{text}\"")
        
        if score == 0.0:
            print(f"Severity Score: {score:.3f} \U0001F7E2 (SAFE - NORMAL TRAFFIC)\n")
        elif score < 0.8:
            print(f"Severity Score: {score:.3f} \U0001F7E1 (WARNING - MODERATE RISK)\n")
        else:
            print(f"Severity Score: {score:.3f} \U0001F534 (CRITICAL - BLACK SWAN EVENT)\n")
