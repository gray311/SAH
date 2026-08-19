---
name: discovery-optimization
description: "Local parameter optimization for step function patterns in C\u2082 maximization. Systematically tune heights and widths within existing pattern families, exploit improvements by drilling down, and diversify across seeds when stuck."
---

# C₂ Optimizer: Local Search Protocol
## Overview
The 13 seed patterns are sophisticated but not globally optimal. Your job is to find LOCAL IMPROVEMENTS by tuning parameters, NOT inventing new architectures.
## Phase 1: Initial Exploration
1. Call param_tuner ONCE to analyze current best and get 3-5 parameter variations
2. For each variation: - Evaluate with evaluate_solution - Track which one improved
3. If ANY improved: SWITCH TO EXPLOITATION mode
## Phase 2: Exploitation (when improvement found)
Given an improved variant:
1. Generate 2-3 FURTHER refinements from THIS variant (not original seed) 2. Evaluate each 3. Keep the best improvement, repeat steps 1-3 4. Continue until: - 3 consecutive no-improvements, OR - You've made 4-5 iterations from this variant 5. THEN switch to a different seed pattern
## Phase 3: Parameter Tuning Details
When generating variations:
- HEIGHTS: Adjust each step height by ±0.02 to ±0.10 from current value - WIDTHS: Shift step boundaries by ±2% to ±5% of the interval width - COMBINATION: Vary both, not just one
Example for pattern with heights [1.40, 1.90, 0.90]: - Variation 1: [1.45, 1.90, 0.85] - Variation 2: [1.40, 1.85, 0.90] - Variation 3: [1.42, 1.88, 0.88]
## Phase 4: Seed Switching
When stuck on one pattern: 1. Note which of the 13 seed patterns you're using 2. After 3 consecutive no-improvements, call param_tuner on a DIFFERENT pattern index 3. Continue Phase 2 on the new seed
## Key Principles
- EXPLOIT before explore: drill down on improvements - Small steps: parameter changes should be subtle (±2-10%) - Multiple evals per variant is OK (3-5) - you need to find the optimum - Don't be afraid to switch seeds - 13 patterns give you plenty to work with
