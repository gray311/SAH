---
name: discovery-optimization
description: "Generate diverse step function candidates with integral=1 constraint. Use sigmoid(latent) scaling to ensure values in [0,1]. Try multiple structural patterns: bipartite, multimodal, piecewise constant, and random with constraint enforcement."
---

# Diversity-First Strategy for Erdos C5

## Step 1: Generate Diverse Candidates

CALL generate_candidates to create 5-7 different step function structures:
- Bipartite: single threshold at a fraction of the domain
- Trimodal: three peaks separated by ~2/5 of domain each
- Piecewise: 3-4 segments with different heights
- Golomb-like: sparse peaks at specific locations
- Random-constrained: random latent, scaled to integral=1

## Step 2: Probe Screening

For each candidate, CALL probe_solution to get approximate c5_bound.
Keep candidates with c5_bound < 0.381 (about 10-15% of candidates).

## Step 3: Full Evaluation

CALL evaluate_solution on the best 2-3 probe candidates.
If any achieves combined_score > 1.0, CALL finish.

## Step 4: Iterate

If no improvement, repeat Step 1 with different structural patterns.

## Critical Rules
- Always use generate_candidates to create VALID candidates (integral=1, values in [0,1])
- Use probe to screen before full evaluation
- Evaluate only candidates with c5_bound < 0.381
- Don't tune hyperparameters until you find viable candidate structures
