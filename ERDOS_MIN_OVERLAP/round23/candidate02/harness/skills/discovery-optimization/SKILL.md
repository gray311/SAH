---
name: discovery-optimization
description: "Use compute_analytical_c5 for exact precomputed c5_bound. Screen 15 seed patterns, evaluate only c5 < 0.37."
---

# Analytical Screening for Erdos Minimum Overlap

## Critical Insight
The seed optimizer has 15 pre-built initialization patterns. Most have c5_bound > 0.37.
You MUST call compute_analytical_c5 on each pattern BEFORE evaluating.

## Workflow

1. CALL compute_analytical_c5 with the seed's best_initialization pattern:
   - Try Golomb with 5-7 marks: [0.0, 0.4, 0.8, 1.2, 1.6] or [0.0, 0.45, 1.0, 1.45, 1.9]
   - Try asymmetric bipartite: h = sigmoid(4*x - 2) or h = sigmoid(3*(x-0.5))
   - Try tri-modal with 5 peaks: centers at 0.35, 0.65, 1.0, 1.35, 1.65

2. FOR EACH PATTERN, call compute_analytical_c5:
   - Get h from sigmoid(latent)
   - Normalize so sum(h)*dx = 1.0
   - Compute c5 = max_k integral h(x)(1-h(x+k))dx via FFT
   - SKIP if c5 >= 0.375 (too bad for full eval)

3. CALL evaluate_solution ONLY on candidates with c5 < 0.36

4. If no improvement after 2-3 evals, try DIFFERENT parameter settings:
   - More/smaller peaks
   - Different spacing
   - Asymmetric designs

## Why This Works
- compute_analytical_c5 gives EXACT c5_bound (matches seed's FFT implementation)
- Screen 15+ patterns cheaply before spending eval budget
- Only evaluate the genuinely promising candidates

## Expected Output from compute_analytical_c5
{"h": [...], "integral": 1.0, "c5_bound": 0.362, "normalized": true}
