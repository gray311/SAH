---
name: discovery-optimization
description: "Optimize programs for the Erd\u0151s minimum overlap problem using bounded local search and probe-based variant ranking."
---

# Erdős C5 Optimization Strategy

## Problem Understanding
- Goal: Minimize max_k ∫ h(x)(1 - h(x+k)) dx
- Current best: 0.380923 → maximize combined_score = 0.380923 / bound
- Constraints: h(x) ∈ [0,1], ∫h(x)dx = 1

## Search Strategy
1. **Start with fewer intervals** (e.g., 50-100) to reduce computation time.
2. **Use local search** to find good breakpoint positions and values.
3. **Probe variants before full evaluation** - use probe_solution to quickly eliminate bad directions.
4. **Incrementally increase intervals** only if it helps.

## Tool Usage
- **probe_solution**: Your primary ranking tool. It's fast (~10s) and uses a separate budget. Call it after each edit to decide whether to invest a full evaluation.
- **evaluate_solution**: Save your budget! Only call after probing shows promise.
- **edit_solution**: Make ONE concrete change per edit. Target the Hyperparameters or core algorithm.

## Common Pitfalls
- Don't use gradient descent with 20,000 steps - too slow, gets stuck.
- Don't evaluate without probing first.
- Don't keep the same number of intervals if full evaluation takes too long.

## Progression
Start simple (few intervals, local search). Probe many variants. Confirm best with full eval. Only then increase complexity.
