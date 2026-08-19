---
name: discovery-optimization
description: "Replace the smooth Gaussian initialization with piecewise-constant constructions using analyze_and_replace_init."
---

# Piecewise-Constant Initialization Strategy

## Why the Seed Fails

The seed's 12 patterns are all smooth (Gaussian, sinusoidal, threshold curves). For the Erdos problem, we need SHARP piecewise-constant functions.

## Workflow

1. CALL analyze_and_replace_init ONCE to get a new piecewise-constant initialization pattern.

2. EDIT the seed to:
   - Replace _get_best_initialization with the tool's suggested code
   - Set num_restarts=1 (we already have the good initialization)
   - Set seed_start=0 (use the first/new initialization)

3. Call evaluate_solution on the edited seed.

4. If score improves, analyze which piecewise structure worked and explore variations.

5. If no improvement, call analyze_and_replace_init again for a different piecewise pattern.

## Expected New Patterns

The tool will suggest constructions like:
- 3-step: high on [0,a], medium on [a,b], low on [b,2]
- 5-step: alternating high/medium/low regions
- Symmetric: high on [0,a] U [2-a,2], medium on [a,2-a]

Success means c5_bound < 0.375 (combined_score > 1.01).
