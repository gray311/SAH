---
name: initialization-strategy
description: Generate diverse latent seeds for the optimizer. Evaluate all candidates fully.
---

# Diverse Initialization Strategy for Erdos Problem

## Why This Approach

The seed optimizer already has:
- 15 different pattern generators
- 59000-step training per candidate
- Integral constraint handling via gradient penalty

The bottleneck is NOT the optimizer - it's getting GOOD initializations.

## Strategy

1. CALL generate_diverse_initializations (temp=0.8)

2. Get 3 latent vectors with DIFFERENT support structures:
   - sparse_concentrated: all energy in left half
   - bimodal: two separated peaks
   - trimodal: three spread peaks

3. CALL evaluate_solution on ALL 3 candidates

4. The optimizer will:
   - Apply sigmoid to get h in [0,1]
   - Train for 59000 steps to minimize C5
   - Satisfy integral(h)=1 via gradient penalty

5. If no improvement, repeat with temp=1.0

## Key Insights

- Don't pre-screen: the optimizer needs to try and validate
- Structural diversity matters more than amplitude
- 3 evals per iteration is affordable (30 total budget)
- Let the optimizer do its job - we just provide diverse seeds
