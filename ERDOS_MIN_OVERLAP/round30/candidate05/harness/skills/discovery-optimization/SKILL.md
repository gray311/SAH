---
name: discovery-optimization
description: "Generate diverse initial step functions via search_patterns, screen with probe_solution, evaluate top candidates. Focus on pattern diversity (Golomb ruler, bipartite, triangular, multi-peak) with exact integral constraint."
---

# Erdos C5 Optimization Strategy

## Phase 1: Pattern Generation (MOST IMPORTANT)

1. CALL search_patterns(temperature=0.5)
   - This generates 5 diverse initial step functions with integral=1
   - Each has precomputed c5_bound via FFT (no training needed)
   - Patterns include: Golomb (well-spaced), Bipartite (single threshold), Triangular, Multi-peak

2. EXAMINE the 5 candidates:
   - Check c5_bound for each
   - Keep those with c5_bound < 0.375

3. CALL evaluate_solution on TOP 2-3 candidates (lowest c5_bound)
   - Full evaluation takes 59000 steps
   - Save probes budget

4. If evaluate shows combined_score <= 1.0 (c5_bound >= 0.381):
   - Try temperature=0.8 with search_patterns again
   - Or try bipartite-only patterns

## Phase 2: Hyperparameter Tuning (only if Phase 1 fails)

If Phase 1 yields no improvement, THEN tune:
- num_intervals: 400, 800, 1600, 3200
- base_learning_rate: 0.001, 0.005, 0.01
- penalty_strength: 40, 80, 120
- num_steps: 30000, 60000

## Key Rules

- ALWAYS use search_patterns FIRST (before any hyperparameter changes)
- NEVER call evaluate_solution on c5_bound > 0.375
- If stuck at combined_score = 0.9999, retry search_patterns with temperature=0.8
- Track best c5_bound across all search_patterns calls
