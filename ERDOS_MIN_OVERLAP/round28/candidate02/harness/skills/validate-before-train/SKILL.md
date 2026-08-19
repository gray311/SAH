---
name: validate-before-train
description: Always validate patterns analytically before training. Use validate_patterns to filter.
---

# Validate Before Training

## Critical Rule

NEVER call edit_solution followed by evaluate_solution without first calling validate_patterns.

## Workflow

1. CALL validate_patterns("pattern_name")
2. Check struct_c5_bound:
   - If >= 0.382: SKIP (pattern fundamentally flawed)
   - If in [0.375, 0.382): TRY WITH LOW CONFIDENCE
   - If < 0.375: PROCEED to training
3. If valid, CALL edit_solution with pattern code
4. CALL probe_solution (fast)
5. If probe good, CALL evaluate_solution

## Why This Matters

- Training 59000 steps on invalid patterns wastes the budget
- validate_patterns is O(1) - instant feedback
- Most seed patterns have struct_c5_bound ~ 0.38-0.40 (useless)
- Only patterns with struct_c5_bound < 0.375 are worth training

## Expected Gain

With validate_patterns, you should find c5_bound < 0.37 candidates in 3-5 evals instead of 20+
