---
name: step-function-explorer
description: Systematically explore step-function parameters for C2 optimization. Use probes first, then evaluate.
---

# Step-Function Explorer Method

## Overview
The current harness stumps at the seed score. To beat 1.03431, you need systematic parameter exploration.

## Core Strategy

1. **START with step_probe (10-15 calls)**
   - Test all 6 pattern types: pyramid, multi_level, asymmetric, single_peak, two_step, custom
   - Vary heights from 1.0 to 2.5
   - Note which pattern types get highest estimates
   - Identify promising height ranges

2. **Refine based on probe results**
   - If pyramid wins: test 5-7 level pyramids with varying step ratios
   - If multi_level wins: test 3-5 levels with ascending/descending height sequences
   - If asymmetric wins: test left-heavy vs right-heavy configurations

3. **Make targeted edits**
   - Focus on ONE parameter that seems important (e.g., middle interval height)
   - Use SEARCH/REPLACE to change just that line
   - Test 3-5 variations

4. **Evaluate the BEST variant**
   - Only after thorough probing
   - Compare to seed score of 1.03431
   - If successful, continue exploring nearby parameter space

## Why This Works

The seed found a good local optimum. To find a better one, you need to:
- Understand what parameter combinations work (probing)
- Focus exploration on promising regions (targeted edits)
- Avoid random mutations that waste evaluations

## Common Patterns to Test

- **Pyramid**: 0.05-0.20-0.40-0.60-0.80-0.95 with heights 0.6-1.3-2.0-1.3-0.6
- **Multi-level**: 0.15-0.25-0.75-0.85 with heights 0.9-1.9-0.9
- **Asymmetric**: 0.10-0.30-0.50-0.70-0.90 with heights 0.7-1.7-1.0-0.7-0.7
- **Two-step**: 0.20-0.45 and 0.55-0.75 with heights 1.5-1.5
- **Custom**: Random 3-5 level functions

## Budget Management

- Use 15-20 evaluations for probing
- Save 10-15 for final refinements and evaluations
- Never evaluate the same code twice
- Stop when you beat 1.03431 or run out of budget
