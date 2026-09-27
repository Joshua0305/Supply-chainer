import sys
import os

# Ensure we can import from backend
sys.path.append(os.getcwd())

import time

def test_live_news_ingestion():
    print("--- SUPPLYCHAINER: LIVE NEWS INGESTION AUDIT ---")
    
    try:
        from backend.engine.news_ingestion import DynamicNewsIngestor
        ingestor = DynamicNewsIngestor()
        
        test_nodes = [
            ("Seattle", "sea"),
            ("Mumbai Port", "sea"),
            ("Suez Canal", "sea"),
            ("Chicago Rail Hub", "rail")
        ]
        
        for node, mode in test_nodes:
            print(f"\nFETCHING: {node} ({mode.upper()})")
            start_time = time.time()
            news = ingestor.get_latest_news(node, mode)
            elapsed = time.time() - start_time
            
            print(f"  Status: {'SUCCESS' if news else 'FAILED'}")
            print(f"  Latency: {elapsed:.2f}s")
            print(f"  Content Snippet: {news[:100]}...")
            
            if "|" in news:
                print("  VERIFIED: Live Multi-headline Ingestion Active.")
            else:
                print("  WARNING: Single headline or fallback detected.")

    except Exception as e:
        print(f"AUDIT FAILED: {e}")

if __name__ == "__main__":
    test_live_news_ingestion()
