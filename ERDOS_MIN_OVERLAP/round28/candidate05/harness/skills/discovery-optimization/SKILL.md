---
name: discovery-optimization
description: "Pattern-first search for Erdos C5. Primary strategy: generate diverse initialization patterns (Golomb, bipartite, tri-modal), screen with probe_solution, evaluate top candidates. Only tune hyperparameters after exhausting pattern space."
---

# Pattern-First Strategy for Erdos C5

## Phase 1: Pattern Exploration (MOST IMPORTANT)

The seed optimizer's 15 patterns may all converge to similar local minima. 
We need FRESH pattern designs to escape this basin.

1. CALL generate_pattern_candidates() ONCE
   - Returns 8 diverse initializations (Golomb, bipartite, tri-modal variants)
   - Each has precomputed integral and c5_bound (no training needed!)

2. ANALYZE the candidates:
   - Filter: keep only those with c5_bound < 0.375 (allows ~5% margin for full eval)
   - Sort by c5_bound (lowest first)

3. CALL evaluate_solution on top 2-3 candidates
   - Only evaluate if probe suggests improvement
   - Stop early if combined_score > 1.0

## Phase 2: Hyperparameter Tuning (SECONDARY)

Only if Phase 1 fails (no improvement in top 5 candidates):

1. Start with BEST pattern from Phase 1 (not seed)
2. Vary ONE hyperparameter at a time:
   - num_intervals: 400, 800, 1600, 3200
   - base_learning_rate: 0.001, 0.005, 0.01, 0.02
   - penalty_strength: 20, 40, 60, 80, 120
   - num_steps: 30000, 59000, 80000
3. Use probe_solution to screen before full eval

## Critical Success Factors

- ALWAYS call generate_pattern_candidates FIRST (not hyperparameter tuning)
- Use probe_solution for ALL pattern candidates (budget ~30 probes)
- Evaluate only top 2-3 after probing
- If no success after 5 patterns with probe screening, try new patterns
