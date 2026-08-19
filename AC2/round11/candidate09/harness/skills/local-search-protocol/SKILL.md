---
name: local-search-protocol
description: Systematic local search around existing step patterns. Tune heights/widths, exploit improvements, switch seeds when stuck.
---

# Local Search Protocol for C₂ Maximization
## Core Principle
Don't try to invent new pattern architectures. The 13 seed patterns are already sophisticated. Your job is LOCAL OPTIMIZATION within these families.
## Phase 1: Initial Exploration
1. Call param_tuner ONCE to get 3-5 parameter variations
2. Evaluate each with evaluate_solution
3. If ANY improved: SWITCH TO EXPLOITATION
## Phase 2: Exploitation
Given an improved variant:
1. Call param_tuner ON THE IMPROVED VARIANT (not the original!) 2. Generate 2-3 refinements 3. Evaluate each 4. Keep the best improvement 5. Repeat steps 1-4 until: - 3 consecutive no-improvements, OR - 4-5 iterations from this variant 6. THEN switch to a different seed pattern
## Parameter Tuning Rules
- HEIGHTS: ±0.02 to ±0.10 per step - WIDTHS: ±2% to ±5% of interval - Vary BOTH height and width parameters
## Seed Switching
When stuck on one pattern: 1. After 3 consecutive no-improvements, switch to a different pattern index 2. Continue Phase 1/2 on the new seed 3. There are 13 patterns - you have plenty to explore
## Key Principles
- EXPLOIT before explore: drill down on improvements - Small steps: parameter changes should be subtle - Multiple evals per variant is OK (3-5) - Switch seeds when stuck, not prematurely
