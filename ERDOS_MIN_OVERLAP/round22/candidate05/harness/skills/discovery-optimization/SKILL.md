---
name: discovery-optimization
description: "Generate many diverse structural initializations for Erdos optimization.\nUse 400 intervals and 2000 steps for rapid evaluation of many candidates."
---

# Structural Diversity Search Strategy

## Why the seed fails
The seed optimizer trains for 120000 steps from a single initialization. This:
- Takes all 30 eval budget on one trajectory
- Gets stuck in local minima
- Never explores different structural forms of h

## New strategy: Evaluate MANY candidates
We can afford fast evaluation with 400 intervals and 2000 steps (~5x faster).
This lets us test 12+ diverse initializations, finding better structures.

## Pattern families to explore

### Golomb ruler patterns
Place spikes at optimal distances: [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75]
- Test with 5, 7, and 9 marks

### Bipartite patterns  
Split [0,2] into [0,a) and [a,2] with different a values
- Try a in {0.3, 0.4, 0.5, 0.6, 0.7, 0.8}

### Tri-modal patterns
Three narrow peaks at different positions
- Centers: [0.3, 1.0, 1.7], [0.2, 1.0, 1.8], [0.4, 1.0, 1.6]

### Threshold patterns
h(x) ≈ 1 for x > t, h(x) ≈ 0 for x <= t
- Try t in {0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8}

### Concentrated mass
All integral mass in a narrow region [c-d, c+d]
- Centers: 0.5, 1.0, 1.5; widths: 0.2, 0.3, 0.4

### Four-partition
h(x) takes 4 different values on intervals
- Try 2+2, 3+1, 1+3 splits

## Workflow

1. Edit hyperparameters: intervals=400, steps=2000, penalty=10.0

2. Add NEW patterns to _get_best_initialization (at least 5-6 new ones)

3. Call generate_candidates(12) with num_candidates=12

4. Call evaluate_solution on each candidate (use all 30 evals)

5. Report best combined_score

## Expected outcome
With 400 intervals and 2000 steps, each eval is ~5x faster.
We can test 12 candidates in 30 evals, finding structural improvements.
