---
name: discovery-optimization
description: "Maximize C2 by creating diverse STEP FUNCTION configurations. The seed has 9 close-but-not-optimal step initializations. Create new ones with varied: step count (2-5), widths (0.2n-0.8n), heights (0.8-2.0), symmetry (centered/asymmetric), and multi-peak patterns. Probe 5-7 variants, eval top 2."
---

# C2 Optimization: Step Function Diversity Protocol

## Objective
Maximize C2 > 1.02872. Current baseline: 1.02872 (seed uses 9 step-like initializations).

## Why Step Functions Win
- Theoretical record: 0.8963
- Seed is ALREADY using step functions (9 initializations)
- The harness failed by mutating optimizer params, NOT step function structure

## Strategy: Diversify Step Function Architectures

### Phase 1: Create Diverse Step Patterns
Don't tweak learning rates. Create NEW step functions:

**Single-Peak Steps:**
- 2-step: f(x) = h for |x| < w, 0 otherwise
- Vary: w = [0.2n, 0.3n, 0.4n, 0.5n, 0.6n], h = [1.0, 1.2, 1.5, 2.0]

**Multi-Peak Steps:**
- 3-step: left, center, right regions with different heights
- Bimodal: two peaks with valley in center
- 4+ step: multiple separated clusters

**Asymmetric Steps:**
- Left-biased: mass concentrated on negative side
- Right-biased: mass on positive side
- Skewed single peak

**Phase Transitions:**
- Flat baseline + elevated region
- Nested rectangles

### Phase 2: Probe & Rank
1. Create 5-7 diverse step configurations
2. Probe each (cheap ~10s, separate budget)
3. Rank by probe score
4. Evaluate TOP 2 only

### Phase 3: If Still Stuck
- Try polynomial: f(x) = exp(-alpha * |x|^beta)
- Try Gaussian mixture: sum of 2-3 Gaussians
- Try hybrid: step base + smooth tails

## Tool Usage
- edit_solution: Write explicit step function code (jnp.where, jnp.piecewise)
- probe_solution: Rank many cheaply
- evaluate_solution: Only for top 2
- finish: When done
