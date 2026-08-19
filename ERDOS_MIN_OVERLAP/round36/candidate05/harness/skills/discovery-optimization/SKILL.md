---
name: discovery-optimization
description: "Generate diverse initial step functions from seed patterns, check integral constraint directly, use low-resolution probing before full evaluation."
---

# Structured Initialization Strategy for Erdos C5

## Why Random Fails
Random hyperparameter tuning doesn't work because:
1. The seed program has BUILT-IN initialization patterns that are more effective than random
2. We need to VARY these patterns, not add random noise
3. Integral constraint (sum(h) = 1) is hard to satisfy with random mutations

## Phase 1: Generate Diverse Initializations

Do NOT call any "analyze" tools. Instead:

1. START with the seed program's _get_best_initialization method
2. VARY the PATTERN PARAMETERS:
   - Threshold patterns: Change threshold values (e.g., x > 0.5 -> x > 0.3, x > 0.7)
   - Multi-modal patterns: Change peak positions (e.g., centers at 0.4,1.0,1.6 -> 0.3,0.9,1.5)
   - Golomb ruler: Change mark positions and widths
   - Bipartite: Change split point (a = 0.5 -> a = 0.3, 0.6, 0.7)

3. Generate 5-10 variants with DIFFERENT parameter combinations

## Phase 2: Quick Integral Check (NO PARSING NEEDED)

For each variant, use the program's OWN methods:
1. Run with num_intervals=100 (faster)
2. Call the program's _compute_c5_bound(h) method
3. Check integral: integral(h) = sum(h) * dx where dx = 2.0 / num_intervals
4. If integral != 1, scale h: h = h / sum(h) * (target_integral / current_integral)

## Phase 3: Low-Resolution Probing

1. Set num_intervals=100, num_steps=5000, penalty_strength=100
2. Run short optimization
3. Call probe_solution to get fast c5_bound estimate
4. If c5_bound < 0.375, proceed to Phase 4

## Phase 4: Full Evaluation

1. Expand to num_intervals=800
2. Set num_steps=120000, penalty_strength=61
3. Run full optimization
4. If combined_score > 1.0, finish

## Key Rules
- NEVER call tools that parse program text (unreliable on JAX)
- ALWAYS vary seed pattern parameters, not random noise
- Use num_intervals=100 for quick screening, 800 for final eval
- Keep penalty_strength high (100+) for low-resolution, moderate (61) for final
- Generate 5-10 diverse candidates before any evaluation
