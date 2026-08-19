---
name: penalty-annealing-strategy
description: Penalty annealing for Erdos optimization - start low penalty to find structure, then tighten constraint. Use with generate_constrained_init() for best results.
---

# Penalty Annealing Strategy for Erdos Minimum Overlap

## Why Annealing Works
- High initial penalty forces integral=1 but constrains optimization too much
- Low initial penalty lets the optimizer find good structural patterns
- Gradual increase balances exploration and constraint satisfaction

## Implementation
In the optimizer's train_step function, compute an annealing schedule:

step_fraction = current_step / total_steps
current_penalty = start_penalty + (end_penalty - start_penalty) * step_fraction

Recommended values:
- start_penalty = 100 (constraints nearly ignored, optimize objective)
- end_penalty = 5000 (strict constraint enforcement)
- total_steps = 50000 (allows smooth transition)

## Workflow
1. Call generate_constrained_init() to get h with integral(h)=1
2. Pass h to optimizer with initial penalty=100
3. Anneal penalty linearly over 50000 steps
4. Extract final h and compute c5_bound
5. Verify combined_score > 1.0

## Debugging
- If combined_score <= 1.0, check: did integral(h) stay close to 1?
- If optimizer diverges, reduce start_penalty to 50
- If final score improved but constraint violated, increase end_penalty to 10000
