---
name: single-pattern-focus
description: Focus on testing ONE pattern at a time with short training runs, then mutate working patterns. Use probe to screen, full eval only for promising candidates.
---

# Single-Pattern Focus Strategy

## Problem with Current Approach

The seed optimizer trains ALL 3 restarts for 59000 steps each. This wastes budget testing patterns that may not work.

## Correct Approach: Test ONE Pattern at a Time

1. **EXTRACT ONE pattern** from the 14 available (e.g., Golomb ruler, tri-modal)

2. **EDIT to use ONLY that pattern**:
   - Remove all other pattern initialization code
   - Set num_restarts=1 (no wasted diversification)
   - Set num_steps=20000 (quick validation)
   - Use num_intervals=800 (default resolution)

3. **PROBE immediately** (do not wait for full eval!)
   - Use probe_solution to get c5_bound
   - If c5_bound >= 0.375: DISCARD this pattern
   - If c5_bound < 0.375: Consider full eval

4. **IF PROMISING (c5_bound < 0.37)**:
   - Call evaluate_solution for final score
   - If combined_score > 1.0: SUCCESS, move to step 5
   - If not: STOP this pattern, try next one

5. **MUTATE WORKING PATTERNS**:
   - Golomb: Change mark positions, spacing, number of marks
   - Tri-modal: Shift peaks, change widths, adjust heights
   - Bipartite: Move threshold, change asymmetry

## Budget Management

- With 60 evals: 15 probe calls, 10 full evals, 35 remaining for mutations
- NEVER do a full eval without probe confirmation first
- Stop exploring a pattern after 1 full eval if not promising

## Pattern Selection Priority

1. **Golomb ruler** (Pattern 12): Well-spaced marks minimize autocorrelation
2. **Tri-modal** (Pattern 14): 3 narrow peaks distribute mass effectively
3. **Bipartite** (Pattern 13): Simple baseline, may be improvable
4. Others only if above fail
