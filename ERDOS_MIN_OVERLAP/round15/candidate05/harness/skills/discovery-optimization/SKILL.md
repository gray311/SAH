---
name: discovery-optimization
description: "Direct construction strategy: bypass slow training, directly construct and FFT-evaluate step function candidates."
---

# Direct Construction Strategy for Erdos Optimizer

## Critical Insight
The seed's optimizer runs 59,000 training steps per evaluation. This is WASTEFUL because the FFT evaluator computes c5_bound in milliseconds.

## New Strategy
1. EDIT to remove the optimizer: Replace the training loop with a direct search over candidate constructions
2. DIRECT CONSTRUCTION: Create step functions analytically (Golomb ruler, bipartite, multi-peak)
3. FFT EVALUATION ONLY: Each candidate evaluated via the FFT formula in ~10ms
4. USE ALL 30 EVALUATION BUDGET to test hundreds of candidates

## Candidate Constructions
Try these patterns (with integral normalization to ensure sum=1):

- Golomb ruler: Points at optimal spacings for 5-7 marks
- Bipartite: h=1 on [0,a] U [2-a,2], h=0 on [a,2-a]
- Tri-modal: Three peaks at specific locations
- Asymmetric: Different heights on different intervals
- Sawtooth: Linear patterns that sum to 1

## Implementation Steps
1. EDIT _get_best_initialization to RETURN A LIST of candidate latents (not just one best)
2. EDIT the main loop to ITERATE over all candidates, computing FFT-based c5_bound for each
3. Pick the best candidate and CALL evaluate_solution once
4. If no improvement, EDIT to add a NEW construction type
