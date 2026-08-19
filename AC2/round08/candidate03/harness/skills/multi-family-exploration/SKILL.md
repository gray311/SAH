---
name: multi-family-exploration
description: Playbook for systematically exploring different function classes to find ones that surpass the seed's 1.034x.
---

# Multi-Family Function Exploration Playbook

## Why the Seed's Approach Isn't Enough

The seed's step functions achieve 1.034x improvement over the theoretical best (0.8963). But 1.0 is the theoretical maximum - you need NEW function classes to bridge the remaining gap.

## The Exploration Protocol

### Phase 1: Family Survey (Iterations 1-5)

1. CALL diversify_function once per iteration with DIFFERENT function_family values
2. For each variant, call probe_solution to get cheap ranking
3. Track which families show promise (combined_score > 1.05 via probe)

### Phase 2: Deepen Promising Families (Iterations 6-12)

1. Pick the 1-2 families with highest probe scores
2. Increase complexity: call diversify_function with higher complexity level
3. Use probe to rank, then evaluate only if combined_score > 1.10 via probe

### Phase 3: Convergence (Iterations 13-20)

1. Evaluate ONLY the top 1-2 variants across ALL families
2. Call finish when you've exhausted the budget or plateau

## Common Pitfalls

- FAILING to change function families: getting stuck in "step function refinement" loop
- EVALUATING too early: waste 10s+ per eval before probing
- STOPPING at seed's performance instead of pushing harder
- NOT tracking which family each probe came from
- Checklist:
  - [ ] Called diversify_function with different families in Phase 1
  - [ ] Probed at least 5 different function classes
  - [ ] Evaluated only 1-2 final candidates
  - [ ] Called finish after budget or clear plateau
