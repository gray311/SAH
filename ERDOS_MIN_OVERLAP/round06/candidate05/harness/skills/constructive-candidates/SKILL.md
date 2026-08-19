---
name: constructive-candidates
description: Generate explicit step function candidates for C₅ bound. Focus on piecewise constant functions with few breakpoints. Prioritize - single-step, double-step, concentrated mass patterns.
---

# Constructive Candidate Generation for C₅

## Core Principle
Build explicit step functions with FEW breakpoints. The optimal h may be simple.

## Template Patterns

### Pattern A: Single Interval
- Breakpoints: [0, 1, 2]
- Values: [2.0, 0, 0] → normalized: h=1 on [0,1], 0 elsewhere

### Pattern B: Two Intervals (Split)
- Breakpoints: [0, 0.5, 1.5, 2]
- Values: [0.5, 0, 0, 0.5] → normalized appropriately

### Pattern C: Concentrated Mass
- Breakpoints: [0, 0.1, 2]
- Values: [10.0, 0, 0] → very narrow spike

### Pattern D: Asymmetric Triple
- Breakpoints: [0, 0.5, 1.0, 2]
- Values: [1.0, -0.5, -0.5, 1.0] → then clip and normalize

### Pattern E: Symmetric Pair
- Breakpoints: [0, 0.66, 1.33, 2]
- Values: [1.5, 0, 0, 1.5] → concentrated at edges

## Optimization Tips

1. Start with 3-5 breakpoints, test integral constraint
2. Use linear scaling: if integral≠1, multiply all values by 1/integral
3. Clip values to [0,1] after normalization
4. Try both concentrated (narrow support) and spread patterns
5. Asymmetric splits often beat symmetric ones

## Common Pitfalls

- Forgetting to normalize → integral≠1 constraint violation
- Values outside [0,1] after normalization → clip them
- Too many breakpoints → overfitting to discretization
- Not testing enough candidates → gradient descent needed exhaustive search

## Success Checklist

[ ] Construct 5-10 diverse candidates
[ ] Each has ∫h=1 (or close, within tolerance)
[ ] Each has h∈[0,1]
[ ] Evaluate each with evaluate_solution
[ ] Track best combined_score
[ ] If any score > 1.0, celebrate!
