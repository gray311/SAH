---
name: simple-structural-search
description: Generate diverse step functions, probe them, evaluate the best.
---

# Simple Structural Search for Erdos C5

## Strategy
Do NOT use correlation analysis or targeted mutations. Instead:

1. CALL search_patterns to get 3-5 diverse step functions
   - Bipartite, multimodal, Golomb-like, random thresholds
   - All satisfy integral(h)=1 and h in [0,1]

2. CALL probe_solution on EACH variant
   - Quick screening (separate budget)
   - Keep those with c5_bound < 0.375

3. CALL evaluate_solution on the 1-2 best probes
   - Full evaluation (consumes real budget)
   - If combined_score > 1.0, finish!

4. If no improvement, REPEAT with new search_patterns call

## Key Rules
- NEVER do correlation_analyzer or targeted mutations
- ALWAYS start with diverse structural variations
- Evaluate only after probing multiple candidates
- Max 3 iterations before restarting
