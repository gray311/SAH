---
name: perturb-seed-patterns
description: Systematically perturb seed program's existing patterns (Golomb marks, bipartite threshold, etc.) and screen with analyze_pattern_effect before full evaluation.
---

# Perturb Seed Patterns for Erdos C5

## Phase 1: Systematic Pattern Perturbation

1. PICK ONE pattern type from seed (golomb, bipartite, triangular, multi_peak)

2. VARY ITS PARAMETERS:
   - Golomb: Try marks [0.0, 0.4, 0.8, 1.6], [0.0, 0.5, 1.0, 1.5], [0.0, 0.33, 0.66, 1.33]
   - Bipartite: Try threshold a in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
   - Triangular: Try center at 0.5, 1.0, 1.5 and widths [0.08, 0.1, 0.12]
   - Multi_peak: Try 2 peaks, 3 peaks, 4 peaks at various centers

3. CALL analyze_pattern_effect with new parameters
   - Each call costs 1 probe (cheap)
   - Get approximate c5_bound

4. KEEP patterns with c5_bound < 0.378 (below seed 0.3809)

5. CALL evaluate_solution on TOP candidate (lowest c5_bound)
   - If combined_score > 1.0, finish
   - If not, pick next parameter variation

6. If stuck after 4 variations, switch to hyperparameter tuning

## Phase 2: Hyperparameter Tuning (last resort)

Tune one parameter at a time:
- num_intervals: 400, 800, 1600 (larger = more resolution)
- penalty_strength: 40, 61, 100, 150 (stronger = stricter integral constraint)
- base_learning_rate: 0.001, 0.004, 0.01
- num_steps: 30000, 60000

Always test ONE change at a time with num_restarts=1, num_steps=30000-60000.
Use probe_solution to screen candidates before full evaluation.
