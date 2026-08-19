---
name: discovery-optimization
description: "Generate diverse pattern-based initializations for Erdos optimization with precomputed analytical scores."
---

# Pattern Initialization Strategy
## Problem The seed optimizer has poor hyperparameters: 800 intervals (slow), penalty=61 (hard constraints).
## Solution: Use generate_candidates Tool
This tool generates 3 structurally diverse initializations with precomputed c5_bound: - Golomb ruler pattern (optimal spacing) - Bipartite pattern (separated support) - Tri-modal pattern (3 narrow peaks)
Each candidate has precomputed integral and c5_bound (no training needed).
## Workflow
1. CALL generate_candidates(temperature=0.7, num_candidates=3)
2. EXAMINE candidates: - Skip if integral != 1.0 (constraint violation) - Skip if c5_bound >= 0.375 (too bad) - Keep if c5_bound < 0.36
3. CALL evaluate_solution on ALL candidates with c5_bound < 0.36
4. If none pass, CALL generate_candidates again with temperature=0.9 for more diversity
## Why This Works - 3 structural diversity: Golomb, Bipartite, Tri-modal - Precomputed scores: no wasted evaluations - Budget-efficient: 1 tool call, 2-3 evals max
