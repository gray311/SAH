---
name: construction-search
description: Systematically explore mathematically principled step function constructions for the Erdos problem. Each construction type is a hypothesis about what optimal h might look like.
---

# Construction-Based Search for Erdos Problem

## Construction Types to Explore
1. **bimodal_tight**: Two narrow peaks at symmetric locations (0.25, 0.75)
   - Good for reducing overlap between h and shifted versions
   - Total integral ≈ 1 by adjusting peak widths

2. **periodic_step**: Alternating step function with 1:2:1 ratio
   - h(x) = 1 on [0.25, 0.75), h(x) = 0 elsewhere

3. **golomb_ruler**: Peaks at optimal Golomb ruler positions
   - Marks at [0, 0.25, 0.625, 0.9375, 1.0] scaled
   - Maximizes minimum distance between peaks

4. **triangular_wave**: Piecewise constant with 3 levels
   - Hierarchy: 0 < 0.5 < 1.0
   - Creates structured correlation patterns

## Execution Plan
For each construction:
1. Use probe_construction tool (zero cost)
2. EDIT _get_best_initialization to use that construction directly
3. CALL evaluate_solution (1 eval each)
4. Track best combined_score

## Key Insight
The seed's 12 init patterns are all sigmoid of random latents.
Optimal h might be a SHARP step function, not a smooth sigmoid.
Replace the sigmoid initialization with direct step function construction.
