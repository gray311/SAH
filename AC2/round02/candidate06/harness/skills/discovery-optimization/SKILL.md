---
name: discovery-optimization
description: "Optimize stepped functions for C\u2082. Explores asymmetric multi-level step functions as the key to exceeding 0.8963. Uses aggressive probe screening (~30 variants) followed by 3-5 full evaluations of best candidates. Focuses on support structure and height ratios."
---

# Stepped Function C₂ Optimization Playbook

## Objective
Beat the current record of 0.8963 by discovering better step-function geometries.

## Core Insight
The current champion (0.8963) uses a SYMMETRIC 1-LEVEL step function. We can beat it by:
- Making it ASYMMETRIC (wider on left/right)
- Adding 2nd and 3rd LEVELS with carefully chosen heights
- Optimizing WHERE the transitions occur

## Phase 1: Asymmetric 2-Level Steps (Probe ~8 variants)

Test these configurations, each with the SAME pattern index but different parameters:

**Pattern 0 (asymmetric left):** Start at 0.2n, end at 0.5n with height 1.1
**Pattern 5 (asymmetric right):** Start at 0.15n, end at 0.55n with height 1.15
**Pattern 8 (two-step with gap):** First step at [0.1n, 0.35n], second at [0.55n, 0.9n]

Vary the height ratio (h from 0.9 to 1.3 in steps of 0.1) and support positions.

## Phase 2: 3-Level Step Functions (Probe ~8 variants)

Create functions with 3 distinct height levels:
- Example: f = [1.2 on [0.1n,0.25n], 1.8 on [0.25n,0.6n], 1.1 on [0.6n,0.85n]]
- Key insight: The MIDDLE level should be the HIGHEST (1.8-2.0 range)
- The transition points should divide the domain in ~1:2:2 ratio

## Phase 3: 4-Level and Beyond (Probe ~6 variants)

- 4 distinct height levels
- Heights typically range: 1.0, 1.2, 1.5, 2.0
- Support should cover 80-90% of the domain

## Phase 4: Support Structure Optimization

For each multi-level function, try:
- Symmetric support: [0.25n, 0.75n]
- Left-heavy: [0.2n, 0.6n]
- Right-heavy: [0.1n, 0.5n]
- Extended: [0.1n, 0.9n]

## Protocol
1. Use probe_solution to test 5-8 variants per configuration
2. Keep the top 3 configurations by probe score
3. Call evaluate_solution on the best variant from each of the top 3 configs
4. Iterate: if no improvement, try a NEW configuration type

## Important Notes
- Do NOT change learning_rate, num_steps, or warmup_steps
- Do NOT try Gaussian mixtures or splines yet
- Focus on STEPS: change start, end, and height values only
- If probe scores plateau, try a completely new support structure

## Success Criteria
- Find ANY variant with combined_score > 1.00384
- This means C₂ > 0.900 (beating the 0.8963 record)
