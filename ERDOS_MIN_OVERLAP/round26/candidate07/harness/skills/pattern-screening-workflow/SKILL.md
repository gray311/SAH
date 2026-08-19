---
name: pattern-screening-workflow
description: Use screen_all_patterns once to test all 15 patterns. Only keep patterns with c5_bound < 0.375. For those, train 10000 steps + probe. Keep c5_bound < 0.372. Then full eval.
---

# Pattern Screening Workflow

## Step 1: Screen All 15 Patterns Analytically

CALL: screen_all_patterns(max_steps=500, threshold=0.375)

This tests ALL 15 patterns from the seed:
- Pattern 0: Normal random
- Pattern 1: Uniform [-2, 2]
- Pattern 2: sin(2πx) + cos(4πx)
- Patterns 3-14: Various scales and shapes
- Pattern 5: Bipartite x<0.5 high
- Pattern 12: Golomb ruler [0,0.4,0.8,1.2,1.6]
- Pattern 14: Tri-modal [0.4, 1.0, 1.6]

Output: List of patterns with c5_bound < 0.375

## Step 2: Refine Promising Patterns

For EACH pattern in results:
1. CALL edit_solution: num_restarts=1, num_steps=10000
2. CALL probe_solution
3. Keep if c5_bound < 0.372

## Step 3: Full Evaluation

For EACH pattern passing Step 2:
1. CALL edit_solution: num_steps=59000
2. CALL evaluate_solution
3. If combined_score > 1.0, you've found a new record!

## Why This Works

- screen_all_patterns tests 15 patterns in ONE tool call
- num_steps=500 is ~1% of full training, but patterns converge fast
- You filter to ~2-4 candidates before spending evals
- Expected: 3-5 evals to find improvement, not 59!

## Example Run

Day 1: screen_all_patterns -> 3 patterns pass c5 < 0.375

Day 2-4: Train 3 patterns 10000 steps + probe -> 1 passes c5 < 0.372

Day 5: Full eval of 1 pattern -> combined_score = 1.05 (NEW RECORD!)

Total evals used: 5 out of 60. 55 evals remaining for search!
