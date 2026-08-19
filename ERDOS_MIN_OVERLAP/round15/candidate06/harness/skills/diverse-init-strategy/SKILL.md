---
name: diverse-init-strategy
description: Use structurally diverse initializations to escape local minima. Screen with probes before full evaluation.
---

# Diverse Initialization Strategy for Erdos Optimizer

## Key Principle
The seed's 12 patterns are all Gaussian/sigmoid-based. To escape,
try INITIALLY DIFFERENT STRUCTURES.

## Workflow
1. Call generate_diverse_init to get 4 new patterns
2. For each pattern, EDIT the seed to use ONLY that pattern:
   - Set num_restarts=1
   - Set seed_start = pattern_index
   - OR better: replace _get_best_initialization to use ONLY that latent
3. Call probe_solution to check:
   - integral(h) ≈ 1 (constraint)
   - c5_bound estimate < 0.37
4. Call evaluate_solution only on candidates with c5_bound < 0.37
5. If no success, ADD a new pattern type (piecewise constant with
   non-Gaussian shape)

## Why This Works
- Golomb ruler patterns have optimal spacing properties
- Bipartite patterns can achieve low overlap by separating support
- Multi-peak patterns can distribute overlap evenly
- Probes let you screen 20+ candidates with the 30-probe budget
