---
name: hill-climbing-erdos
description: Refine a good Erdos candidate using targeted mutations. Use when probe_score < 0.38. Try peak shifts, splits, merges. Always maintain integral=1.0.
---

# Hill-Climbing for Erdos Optimization

## When to use this skill
Use after generate_single_candidate returns a candidate with:
- integral ≈ 1.0
- c5_bound_approx < 0.38

## Mutation Types (try in order)

### 1. Peak Shift
- Select the peak that contributes most to overlap
- Shift it by ±0.05, ±0.1, ±0.15
- Re-normalize to maintain integral=1.0
- Call probe_solution after each shift

### 2. Peak Split
- If a peak is wide (>0.25 width), split into two
- Place new peak at ±0.08 from original
- Scale heights to maintain integral

### 3. Peak Merge
- If two peaks are close (<0.2 apart), merge them
- Place new peak at midpoint
- Scale height appropriately

### 4. Peak Height Adjustment
- Increase height of smallest peak
- Decrease height of largest peak
- Re-normalize

## Validation After Edit
- Check integral is still ~1.0
- Check h values in [0,1]
- Call probe_solution to verify improvement

## Example Workflow
1. Candidate has 2 peaks at [0.2, 1.8]
2. Shift first peak to 0.25
3. Call probe_solution: c5 = 0.375 (improvement!)
4. Call evaluate_solution for full score
5. If better, keep and iterate

## Budget Tip
- Use 2-3 probe calls before 1 full eval
- Stop when c5_bound_approx >= 0.38
