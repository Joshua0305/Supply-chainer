import feedparser
import urllib.parse
import time
import socket
from typing import List, Dict

class DynamicNewsIngestor:
    """
    Supplychainer Stage 1: Dynamic News Ingestion.
    Consumes live external intelligence from Google News RSS.
    Implements location-aware text retrieval and caching.
    """
    def __init__(self):
        self.cache = {} # {query: (timestamp, content)}
        self.cache_ttl = 900 # 15 minutes
        
        # Operational Physics Fallbacks (Offline Reliability)
        self.fallback_news = {
            "sea": "Maritime congestion reported at major transshipment hubs. Berthing delays expected.",
            "air": "Aviation fuel surcharge volatility and cargo handling backlogs noted in international airports.",
            "road": "Highway traffic density increasing in primary logistics corridors.",
            "rail": "Rail freight scheduling adjustments due to infrastructure maintenance."
        }

    def get_latest_news(self, location: str, transport_mode: str) -> str:
        """
        Fetches live news for a specific geographic node and transport mode.
        """
        query = f"{location} {transport_mode} logistics disruption"
        
        # 1. Check Cache
        now = time.time()
        if query in self.cache:
            ts, content = self.cache[query]
            if now - ts < self.cache_ttl:
                return content

        # 2. Live Ingestion (Google News RSS)
        t_start = time.perf_counter()
        print(f"[TRACE] STEP 7: News ingestion started for {location}")
        try:
            encoded_query = urllib.parse.quote(query)
            rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
            
            # Set a hard timeout for the socket
            socket.setdefaulttimeout(2.0)
            
            feed = feedparser.parse(rss_url)
            
            if feed.entries:
                top_headlines = [entry.title for entry in feed.entries[:3]]
                content = " | ".join(top_headlines)
                self.cache[query] = (now, content)
                print(f"[TRACE] STEP 8: News ingestion complete ({time.perf_counter()-t_start:.4f}s)")
                return content
            
        except Exception as e:
            print(f"[TRACE] News ingestion error for {query}: {e}")
            
        # 3. Defensive Fallback
        print(f"[TRACE] STEP 8: News ingestion complete (Fallback used)")
        return self.fallback_news.get(transport_mode.lower(), "Normal operational conditions reported.")
