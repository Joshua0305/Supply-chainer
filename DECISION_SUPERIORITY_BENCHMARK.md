Multimodal Network: 300 nodes, 1054 edges
Calibration Layer: Loaded 4 mode profiles from historical p5/p95 analysis.
Supplychainer V3 Brain Loaded: Production-Ready.
NLP Brain: Loaded Historical Anchor Matrix.
NLP Brain: Loaded Historical Anchor Matrix.
NLP Brain: Loaded Historical Anchor Matrix.
# DECISION SUPERIORITY BENCHMARK SUITE
## Supplychainer V3: The Logistics Source of Truth

This document serves as proof-of-concept for the Decision Superiority of Supplychainer's 4-stage Threat Intelligence pipeline.

---

### [1] SUEZ FAILURE SCENARIO: Reroute Survival
**Route:** Shanghai -> Rotterdam
**Disruption:** CRITICAL: Suez Canal blocked by massive container vessel.

| Metric | Naive Baseline (Static) | Supplychainer (Dynamic) |
| :--- | :--- | :--- |
| **Primary Route** | via Suez Canal | via Cape of Good Hope |
| **Status** | ✗ TRAPPED | ✓ OPERATIONAL |
| **Adjusted ETA** | ∞ (Halted) | 500.9h |
| **p85 Delay Risk** | Unknown | 145.0h |
| **Decision Logic** | Shortest path geometry | Worst-case p85 optimization |

**Why Google Maps fails here:**
Google Maps/Naive systems use static geometry. They route into the 400-ship backlog because Suez is the 'shortest' geometric path.

**Supplychainer Logic:**
Strategic buffer of 144.96h added based on live news-correlated operational volatility.
*Redirected to PORT-ROTTERDAM corridor to avoid identified systemic blockage.*

---

### [2] AIR VS SEA ECONOMICS: High-Value Optimization
**Routes Compared:** 
- Sea: Mumbai -> Rotterdam (Sea, General)
- Air: Mumbai -> Frankfurt (Air, High-Value)

| Metric | Naive Baseline (Sea) | Supplychainer (Air Preferred) |
| :--- | :--- | :--- |
| **ETA** | 324.7h | 29.1h |
| **Freight Cost** | LOW ($) | PREMIUM ($$$) |
| **Hidden Risk** | High (Visibility Gap) | Low (Velocity Guarded) |

**The Superiority Factor:**
Supplychainer's model identifies that for high-value cargo, the 'inventory carry cost' (the cost of capital tied up during a 30-day sea transit) combined with the p85 volatility risk makes Sea a sub-optimal business decision.

**Supplychainer Logic:**
Supplychainer automatically identifies that for 'high_value' cargo, the inventory carry cost and p85 disruption risk in sea transit outweigh the air freight premium. It forces a modal shift to preserve capital velocity.

---

### [3] CARF FALSE ALARM REJECTION: Precision Intelligence
**Route:** LA -> Chicago (Rail)
**Mode:** Rail
**Disruption Signal:** "Major port strike at Los Angeles. All container terminals closed. 20 vessels anchored off-shore."

| Metric | Naive Baseline (Simple NLP) | Supplychainer (CARF) |
| :--- | :--- | :--- |
| **Reaction** | PANIC REROUTE / DELAY | MAINTAIN VELOCITY |
| **Delay Added** | High (False Match: 'LA') | 11.6h (Systemic Floor) |
| **Precision** | Low (Location Only) | High (Modality + Context) |

**The Superiority Factor:**
Simple systems see "LA" and "Strike" and panic. They don't understand that a port strike doesn't stop a train on the BNSF corridor.

**Supplychainer (CARF) Logic:**
CARF (Context-Aware Relevance Filter) identified the threat as SEA-specific ('vessels', 'terminals'). It rejected the alarm for the RAIL leg, maintaining full velocity while competitors stalled.

---

## FINAL VERDICT
It is irrational for enterprise logistics teams to use static routing systems. Supplychainer provides **Decision Superiority** by transforming messy, global disruption news into deterministic, physics-aware routing instructions.

