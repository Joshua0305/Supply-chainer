# Supplychainer: Context-Aware Agentic Routing Engine

> **An NLP-driven Risk Assessment API & Executive Command Dashboard for Dynamic Supply Chain Graph Routing.**

Traditional supply chain routing algorithms (like Dijkstra or A*) rely on static distances. But in the real world, supply chains are disrupted by dynamic **Black Swan events**—hurricanes, worker strikes, and geopolitical blockades. 

**Supplychainer** is a dual-component platform:
1. **Agentic AI Backend**: Intercepts route requests, reads live global news along the path, applies logical context filters, and mathematically calculates the **85th-percentile worst-case delay**.
2. **Executive Command Dashboard**: A high-performance, multimodal React frontend to visualize risks, trigger live simulations (like a Suez blockage), and perform comparative intelligence auditing.

---

##  Key Features

* **Real-time Threat Intelligence**: Monitors global RSS feeds to detect local disruptions before they trap inventory.
* **Context-Aware Relevance Filter (CARF)**: Eliminates false positives (e.g., ignoring a seaport strike if the transport mode is Rail).
* **Quantile ML Risk Assessment**: Uses a Gradient Boosting Regressor trained on 50,000+ real-world historical incidents to predict the **worst-case p85 scenario buffer**, not just the mean delay.
* **Executive Dashboard**: A visually stunning 3-column command interface featuring real-time tradeoff strips, operational configuration drop-downs, and forensic audit trails.

---

##  The Architecture Pipeline

Our system decouples sensory data from mathematical risk using a 4-stage pipeline:

1. **The Targeted Fetch:** The routing algorithm requests a path (e.g., Shanghai to Rotterdam). The API evaluates the Origin, Destination, and dynamic Choke Points.
2. **The Sensory Brain (Contrastive NLP):** We utilize a `SentenceTransformer` (`all-MiniLM-L6-v2`) with **Contrastive Semantic Anchoring**. It reads live news texts, splits them via semantic chunking, and calculates a pure "Threat Margin" against a multi-domain matrix of Disasters vs. Safe baseline scenarios.
3. **The Logic Gate - CARF System:** The **CARF** prevents hallucinated delays. If the news reports a *sinking ship*, but the transport mode is an *EV Delivery Van*, CARF zeroes out the threat. It ensures spatial and modal relevance.
4. **The Decision Brain - Quantile ML:** The context-filtered NLP score, combined with tabular operational data, is fed into a **Gradient Boosting Regressor**. We use a `Quantile Loss` function (alpha=0.85) to predict the worst-case scenario buffer.

---

##  Project Structure

```
Smart_Supply_Chain/
├── backend/
│   ├── main.py                  # FastAPI app + all HTTP/WebSocket routes (the real entry point)
│   ├── requirements.txt
│   ├── data/
│   │   ├── canonical_hubs.json       # ~300 real-world ports/airports/rail yards/road hubs
│   │   ├── canonical_locations.json  # city -> per-mode hub lookup
│   │   └── suppliers.json            # sample supplier records for Supplier Intelligence
│   └── engine/
│       ├── multimodal_network.py     # builds the routable graph from canonical_hubs.json
│       ├── route_recommender.py      # Dijkstra routing + persona weighting (the core solver)
│       ├── threat_intelligence.py    # NLP threat scoring + CARF filter + ML quantile predictor
│       ├── news_ingestion.py         # live RSS pull with an offline fallback per mode
│       ├── scenario_manager.py       # the 6 scripted disruption scenarios
│       ├── supplier_scorer.py        # supplier ranking + procurement advice
│       ├── node_resolver.py          # resolves a city/hub name to a graph entry node
│       └── (baseline.py, graph_model.py, simulator.py, optimizer.py, evaluator.py,
│            benchmark_runner.py, or_baseline.py, weather_integration.py, live_routing.py)
│            — an earlier, US-only prototype pipeline. Not used by the live app — see below.
├── Execution/
│   ├── risk_model.pkl             # trained Gradient Boosting quantile regressor
│   ├── label_encoders.pkl         # categorical encoders for the model above
│   ├── nlp_anchors.pt             # precomputed disaster/safe embedding anchors
│   ├── calibration_profiles.json  # per-mode floor/cap delay calibration
│   └── api.py                     # an older, standalone prototype API — not used by main.py
└── frontend/
    ├── package.json, vite.config.js
    └── src/
        ├── App.jsx                   # top-level view switcher
        ├── RouteRecommender.jsx      # main routing dashboard (calls /api/recommend)
        ├── SupplierIntelligence.jsx  # supplier ranking dashboard (calls /api/suppliers)
        └── BenchmarkCharts.jsx       # static, hardcoded benchmark charts — not live-wired
```

**Two things that look like the main entry point but aren't, so you don't lose time in the wrong file:**
- `Execution/api.py` is an older, standalone prototype with its own `/predict_route_risk`
  endpoint. The real, live API is `backend/main.py`.
- The following files under `backend/engine/` belong to an earlier, US-only prototype and are
  **not** wired into `main.py`'s actual request path: `baseline.py`, `graph_model.py`,
  `simulator.py`, `optimizer.py`, `evaluator.py`, `benchmark_runner.py`, `or_baseline.py`,
  `weather_integration.py`, `live_routing.py`. The live system is the `RouteRecommender` /
  `ThreatIntelligencePredictor` / `multimodal_network` pipeline described above — that's where
  your time is best spent.

---

##  Decision Superiority Benchmarks

Supplychainer shifts logistics from geometric shortest paths to optimal business decisions:
* **Suez Canal Failure**: Reroutes automatically via Cape of Good Hope, avoiding infinite delay backlogs.
* **Air vs. Sea Economics**: Shifts high-value cargo to Air when the p85 risk of Sea transit (and inventory carry cost) outweighs the freight premium.
* **Zero Latency Scaling**: With our static + dynamic risk overlay, multimodal routing latency dropped by **86%** (from 15s to ~2s per request).

---

##  How to Run Locally

### 1. Backend Service (FastAPI)

Run everything from the **project root** (this folder, `Smart_Supply_Chain/`) — not from inside
`backend/`. `backend/main.py` uses relative imports (`from .engine...`), which only resolve
when it's imported as part of the `backend` package, and its model-loading code references
`./Execution/risk_model.pkl` relative to the working directory you launch from. Both of those
require the project root as your working directory.

The ML model (`risk_model.pkl`) and categorical encoders (`label_encoders.pkl`) are pre-trained and included in `Execution/`. You **do not** need the proprietary CSV dataset to run the API.

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```
*The first boot may take 10-20 seconds to load the HuggingFace transformer weights into memory. API Docs available at `http://127.0.0.1:8000/docs`.*

### 2. Executive Frontend (React/Vite)

```bash
cd frontend
npm install
npm run dev
```
*Access the dashboard at `http://localhost:5173` (or the port specified by Vite).*

---

##  API Usage Example

**Endpoint:** `POST /api/recommend`
*(this is what the Executive Frontend actually calls — see `frontend/src/RouteRecommender.jsx`)*

**Payload:**
```json
{
  "source": "Shanghai",
  "destination": "Rotterdam",
  "cargo_type": "general",
  "priority": "normal",
  "transport_preference": "any",
  "routing_policy": "STRICT",
  "scenario": "SUEZ_BLOCK"
}
```

**Response** (abbreviated — `recommendations` holds up to 3 persona-optimized routes, each with a full multi-leg `legs` array and `audit_trace`):
```json
{
  "origin": "Shanghai",
  "destination": "Rotterdam",
  "active_scenario": "Suez Canal Blockage",
  "recommendations": [
    {
      "persona": "BALANCED",
      "legs": [
        { "to_name": "Suez Canal", "mode": "SEA", "eta": 306.3, "threat": 1.0,
          "reason": "Vessel grounding in Canal Narrows. Canal authority estimates 10-day salvage window.",
          "intel_source": "SCENARIO" },
        { "to_name": "Port of Rotterdam", "mode": "SEA", "eta": 61.5, "threat": 0.0,
          "reason": "Maritime congestion reported at major transshipment hubs. Berthing delays expected.",
          "intel_source": "FALLBACK" }
      ],
      "adjusted_eta": 649.9,
      "total_cost": 2603.67,
      "threat_level": 1.0,
      "explanation": "Economic-optimized. Multimodal balance reduces total landed cost by 396% vs premium express AIR, while maintaining defensible lead times."
    }
  ]
}
```
*(Captured from a real run against the trained model and canonical hub graph — not illustrative placeholder data.)*

There's a second, older prototype endpoint, `POST /predict_route_risk` in `Execution/api.py`. It is **not** part of the live app (nothing imports or serves it from `backend/main.py`) — it's a standalone leftover from an earlier iteration and isn't wired to the frontend.

---

## 💻 Tech Stack

* **Frontend**: React, Vite, Vanilla CSS (Executive Dark-Mode Aesthetic)
* **Backend**: FastAPI, Python, Uvicorn
* **Machine Learning**: Scikit-Learn (Gradient Boosting with Quantile Loss)
* **NLP**: HuggingFace Sentence-Transformers
* **Data Ops**: Pandas, NumPy, NetworkX

---

##  TatHack Prelim Challenge

This repository is your starting point. There are two things to work on, and you're free to
lean into either or both:

**1. Fix what's broken.** The codebase has a handful of intentionally introduced issues. None
of them crash the app or throw a visible error — they're logic bugs that quietly produce the
wrong number or the wrong decision while everything still "runs fine." Don't trust that a
feature works just because it doesn't error out: test it against a real scenario (for example,
activate the `SUEZ_BLOCK` scenario in the dashboard and check whether the reported threat and
delay actually reflect it) and check the numbers, not just the absence of a crash.

**2. Build what's missing.** Pick one or more ideas from the list below — or bring your own —
and extend the platform. We're not scoring on how many features you bolt on; we're scoring on
whether what you build is genuinely useful, correctly wired end-to-end (not just a UI mockup),
and whether you can explain the trade-offs you made.

---

##  Where You Can Take This

Supplychainer is a working prototype, not a finished product. Here's where the biggest
opportunities are if you want to push it toward something a real logistics team could rely on
— pick what's interesting, you don't need to attempt all of it:

### Smarter AI/ML
- **Wire the trained ML model into live routing.** `ThreatIntelligencePredictor.predict_worst_case_delay()`
  — the p85 quantile model — is loaded and warmed up at startup but never actually called by
  `RouteRecommender.recommend()` today. Only the NLP+CARF semantic score currently feeds route
  weighting. Connecting the model's real delay prediction into the routing decision is one of
  the most meaningful upgrades available in this codebase.
- Predict multiple quantiles (p50 / p85 / p95) instead of a single point estimate, for a
  confidence band instead of one number.
- Add real explainability (e.g. SHAP or permutation importance) to the model's predictions,
  surfaced through the existing `audit_trace`.
- Generalize `CARFFilter` to rail and road with the same rigor it already applies to air/sea —
  it defines relevance keywords for all four modes but only enforces two of them today.
- Categorize threat *type* (strike / weather / geopolitical / infrastructure), not just
  magnitude, so downstream logic can react differently to different kinds of disruption.

### Product & Experience
- Replace the placeholder map text in `App.jsx`'s default view with a real interactive map
  (Leaflet/Mapbox) driven by the existing `/api/network` endpoint.
- Route history — persist and compare past recommendations instead of losing them on refresh.
- Export a route's full audit trail as PDF/CSV for a "boardroom-ready" report.
- Real-time alerts when a newly activated scenario affects a route you've already generated.
- A mobile-responsive layout — the current dashboard assumes a wide desktop screen.

### Global Reach & Data Coverage
- Expand beyond the current ~300 canonical hubs to more regions and secondary ports/airports.
- Multi-language UI — the dashboard is English-only right now.
- Multi-currency cost display instead of a single implicit currency.
- Replace or augment Google News RSS with a richer, more verifiable disruption signal (e.g.
  structured event feeds, AIS vessel tracking, region-specific weather alerts).
- Accessibility: keyboard navigation, screen-reader labels, color-contrast-safe risk indicators.

### Reliability & Scale
- Persist state in a real database instead of in-memory Python objects — right now a restart
  wipes everything, and there's no per-user or per-company data isolation.
- Add authentication and basic multi-tenancy.
- Add automated tests — there currently aren't any, for either the backend or the frontend.
- Cache or pre-compute more of the graph-weighting work so the engine scales past a few
  hundred nodes without the per-request cost growing with it.

### Integrations
- A webhook or export format a real TMS/ERP system could actually consume.
- An API key / rate-limiting layer, if this were ever exposed publicly.

*In association with Arvind and TatHack Team.*
