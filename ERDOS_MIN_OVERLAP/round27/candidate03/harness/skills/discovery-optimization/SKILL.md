---
name: discovery-optimization
description: "Pattern mutation strategy for Erdos C5. The seed has 15 initialization patterns. Mutation generates variants: Golomb (4-5 marks), Tri-modal (3 peaks), Bipartite. Each variant is integral-normalized (sum*h*dx=1) before evaluation. Use probe to filter c5_bound < 0.375, then full eval."
---

# Pattern Mutation Strategy for Erdos C5 Problem

## Core Idea
The seed optimizer's 15 initialization patterns are promising. We mutate them to narrow peaks, adjust spacing, add/remove marks.

## Step 1: Generate Pattern Variants
1. CALL pattern_mutation_generator() ONCE - get 3-4 integral-normalized variants
2. Variants include: Golomb-4, Golomb-5, Tri-modal-3, Bipartite
3. Each has integral check: sum(h)*dx ~ 1.0 (if not, skip)
4. Check c5_bound in output (analytical, no training)

## Step 2: Filter by Probe
- KEEP if c5_bound < 0.375 (tight margin from current best 0.3809)
- SKIP if c5_bound >= 0.38 (likely won't beat seed after training)

## Step 3: Quick Training
For each kept variant:
- Set num_restarts=1, num_steps=30000
- This quickly trains the variant and checks if training improves it
- Call probe_solution to check c5_bound before full eval

## Step 4: Full Evaluation
If probe shows c5_bound < 0.381 (combined_score > 0.9998):
- Call evaluate_solution with num_restarts=1, num_steps=30000
- Report combined_score

## Step 5: Iterate
If no improvement, mutate patterns differently:
- Golomb: try 4 marks vs 5 marks
- Tri-modal: try different peak centers [0.3,1.0,1.7] vs [0.4,1.0,1.6]
- Bipartite: try a=0.45 vs a=0.55 vs a=0.65

## Why This Works
- Pattern mutations are BETTER than random Gaussian
- Integral normalization ensures constraint satisfaction
- Quick training (30k steps) filters promising variants
- Only waste full evals on near-winners
