---
name: erdos-optimization-strategy
description: Optimize Erdos minimum overlap by generating diverse step function constructions, probing variants cheaply, then refining top candidates with gradient descent.
---

# Erdos Minimum Overlap Optimization Strategy

## Problem
Find h: [0,2] -> [0,1] minimizing max_k integral(h(x)*(1-h(x+k))) dx, subject to integral(h) = 1.
Target: beat C5 <= 0.38092303510845016 (combined_score > 1.0).

## Key Insight
Gradient descent alone gets stuck in local minima. Use construction diversity + cheap probing.

## Method
1. Generate 3-5 diverse variants using generate_variants:
   - Block-based partitions (4 blocks with varying heights)
   - Sine modulation: h(x) = 0.5 + A*sin(B*x)
   - Two-bump construction: mass in two regions
   - Random perturbations from known seeds
   - Refined blocks with smooth transitions

2. Probe all variants with probe_solution (cheap, ~2000 rows):
   - Rank by approximate score
   - Select top 2-3 candidates

3. Refine top candidates with targeted edit_solution:
   - Adjust learning_rate (0.003-0.005), num_steps (15000-20000), penalty_strength (800k-2M)
   - Run for 15000-20000 steps
   - Use smaller learning rate for fine-tuning

4. Evaluate finalists with evaluate_solution:
   - Each costs 1 of 20 evaluations
   - Track best combined_score
   - Must exceed 1.0 to beat current bound

## Pitfalls
- validity = 0: Check sigmoid clipping, integral constraint violation
- Low scores: Try different construction method entirely
- Timeouts: Reduce num_intervals or num_steps
- Stalling: Reset to fresh construction after 5 iterations

## Tool Usage
- generate_variants(num=5) -> diverse code snippets
- probe_solution -> quick ranking of snippets
- edit_solution -> insert chosen snippet into EVOLVE-BLOCK
- evaluate_solution -> official score
- finish -> end when done"
