---
name: jump-pattern-search
description: Generate multiple structurally diverse candidates using jump_to_pattern and evaluate the best.
---

# Jump-to-Pattern Search Strategy

The seed optimizer trains on ONE candidate for 59000 steps.
To improve, we need to try MANY different starting structures.

## Workflow

1. Generate 4-6 candidates with different structures:
   - two-level: simple bipartite split
   - three-level: three regions with varying heights
   - golomb: peaks at specific marks
   - sinusoidal: wave-like modulation

2. Analyze c5_bound from each candidate (precomputed, no training)

3. Filter: keep candidates with c5_bound < 0.36

4. CALL evaluate_solution on all kept candidates

5. If no improvement, try different seeds or structures

## Example Output

Candidate 0 (two-level): integral=1.00, c5=0.358 -> EVALUATE
Candidate 1 (three-level): integral=1.00, c5=0.362 -> EVALUATE
Candidate 2 (golomb): integral=1.00, c5=0.371 -> SKIP
Candidate 3 (sinusoidal): integral=1.00, c5=0.365 -> EVALUATE

This gives us 3-4 full evaluations per batch.
