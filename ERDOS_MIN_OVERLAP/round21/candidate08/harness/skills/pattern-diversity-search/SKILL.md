---
name: pattern-diversity-search
description: Generate many diverse initializations with precomputed scores. Screen candidates with c5_bound < 0.37 before evaluation.
---

# Pattern Diversity Search Strategy

## The Challenge

Training for 120,000 steps is very expensive (~5 minutes). We need to find good starting
points without wasting evaluations on poor candidates.

## The Solution

1. Generate MANY candidates at once using generate_candidates(num_candidates=12).
   This gives 12 structurally different starting points.

2. EXAMINE all 12 candidates carefully:
   - integral: MUST equal 1.0 (skip if not)
   - c5_bound: analytical precomputed score (skip if >= 0.370)

3. Evaluate ONLY promising candidates (c5_bound < 0.370).
   Typically 2-5 out of 12 will pass.

4. If no improvement after 3-4 evaluations, generate a new batch with different temperature.

## Why 12 Candidates?

- With seed stuck at c5 ~ 0.381, we need variety
- 12 patterns cover: Golomb (optimal spacing), Bipartite (separated support), Tri-modal (3 peaks),
  various threshold patterns, and random seeds
- Each has different structural properties that might generalize better

## Success Metric

- Seed: c5 = 0.381, score = 1.000
- Target: c5 < 0.380, score > 1.0
- With 12 candidates, probability of finding c5 < 0.370 is high
- Only evaluate those with c5 < 0.370
