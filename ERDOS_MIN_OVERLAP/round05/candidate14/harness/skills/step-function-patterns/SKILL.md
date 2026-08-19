---
name: step-function-patterns
description: Playbook for constructing step functions that satisfy ∫h=1 and minimize max_k ∫h(x)(1-h(x+k))dx. Focus on discrete piecewise constant patterns rather than continuous optimization. Try uniform, clustered, periodic, and asymmetric structures systematically.
---

# Step Function Pattern Library

## Pattern 1: Uniform Steps
Equal-width steps with equal heights. Simple baseline.
- h(x) = c for all x
- Constraint: c × 2 = 1 ⇒ c = 0.5
- Expected: Good baseline, may not beat 0.3809

## Pattern 2: Clustered Mass
Concentrate most mass in one region to minimize overlap elsewhere.
- Example: h(x) = 2 for x∈[0,0.5], 0 elsewhere
- But must satisfy ∫h=1, so adjust heights
- Try: high value in [0,0.5], low in [0.5,2]

## Pattern 3: Periodic Pattern
Alternating high/low regions that create less overlap.
- Example: h(x) = 0.8 for x∈[0,1], 0.2 for x∈[1,2]
- Check overlap structure

## Pattern 4: Asymmetric
Unequal regions with tailored values.
- Try concentrating mass where the overlap kernel is weakest

## Pattern 5: Multi-step Custom
Fine-tune with 4-6 steps, optimizing both positions and values.
- Use the code generator with num_steps=4-6

## Evaluation Guidance

1. Start with 2-3 simple patterns to establish baselines
2. Use probe_solution to quickly test ~5-10 variants
3. Pick top 2-3 for full evaluation
4. If no improvement after 15 evals, try a fundamentally different pattern
5. Remember: you're finding a SPECIFIC function, not optimizing parameters

Key insight: The discrete combinatorial structure matters more than fine-tuning.
Try many different "shapes" before refining.
