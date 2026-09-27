# JUDGE HOSTILE ATTACK SUITE - REPORT
Engine Cold Start Latency: 0.521s

## TEST GROUP 1 — Fake Persona Detection
### A. Domestic Corridor (DC-KOCHI -> PORT-CHENNAI)
Returned 2 personas. Latency: 0.013s
**PASS**: No fake duplicates. Structural deduplication active.
### B. Global Corridor (PORT-SHANGHAI -> PORT-ROTTERDAM)
Returned 1 personas. Latency: 0.011s
**PASS**: Personas are structurally unique or correctly suppressed.

## TEST GROUP 2 — Scenario Credibility Attack
### A. Normal Conditions (PORT-SHANGHAI -> PORT-ROTTERDAM)
**PASS**: Normal route accurately traverses CHOKE-SUEZ constraint.
### B. SUEZ_BLOCK Scenario
Solve Latency: 0.010s
**PASS**: Scenario structurally rerouted the physical path.

## TEST GROUP 3 — Impossible Route Truthfulness
### A. STRICT ROAD (India -> USA)
**PASS**: Rejected gracefully with exact operational reasons: {"road": "Graph disconnected: No path between DC-KOCHI and HUB-LOSANGELES."}
### B. STRICT AIR -> ROAD-ONLY Node
**PASS**: Rejected explicitly. Details: {"air": "Destination resolution failed: STRICT AIR mode unavailable for DC-CHICAGO"}

## TEST GROUP 4 — Transfer Integrity
### A. STRICT ROAD (AIR-COK -> PORT-CHENNAI)
**PASS**: Explicit transfer leg visible. No cargo teleportation from Airport to Highway.

## TEST GROUP 5 — Executive Explainability Attack
### A. Reasoning Verification
**PASS**: Deterministic reasoning detected: 'Optimized purely for minimum ETA. Recommended for urgent freight with high risk tolerance.'

## TEST GROUP 6 — Latency Credibility
### A. Solve Metrics
- Cold Start: 0.521s
- Warm Solve (Domestic): 0.013s
- Warm Solve (Global): 0.011s
- Scenario Injection Solve: 0.010s
**PASS**: Engine operates at near-instant O(1) overlay speeds. Judge stable.