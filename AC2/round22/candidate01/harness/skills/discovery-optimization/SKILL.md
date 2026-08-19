---
name: discovery-optimization
description: "Pattern-space exploration for step-function C2 maximization. Generate diverse step patterns, rank with probes, then refine."
---

# C2 Maximizer: Pattern-Space Exploration Protocol

## Core Principle
The seed has 12 parameterized step patterns. They can be GENERATED, RANKED, and REFINED. DO NOT try to parse/edit the seed directly - USE generate_step_pattern_probes to get ready-to-evaluate variants.

## Phase 1: Pattern Generation and Probe Ranking (iterations 1-10)

Step 1: Generate Pattern Pool
- Call generate_step_pattern_probes(10) to generate 10 diverse patterns from the seed's pattern space
- This returns ready-to-evaluate step functions with different heights, widths, and multi-level structures

Step 2: Probe All Patterns
- Call probe_solution on ALL 10 generated patterns (10 probes)
- Rank by probe score (higher is better)

Step 3: Full Evaluation
- Call evaluate_solution on TOP 2 by probe score
- If either beats record (c2 > 0.8962799441554086): switch to Phase 2 with best pattern
- If no improvement: expand pattern pool (iterate pattern_idx 0-11 systematically)

Step 4: Iterate
- If no improvement after 3 iterations: try Phase 3

## Phase 2: Parameter Refinement (iterations 11-20)

Step 1: Generate Refined Patterns
- Call generate_step_pattern_probes(5) with refinements to winning pattern
- Variations: adjust peak heights by +/-0.1, expand/contract peak width by 5%

Step 2: Probe and Evaluate
- Probe all 5, evaluate best
- Use JAX gradients if available to guide refinements

Step 3: Continue Until Budget Exhaustion

## Phase 3: Aggressive Re-Exploration (iterations 21-30)

Step 1: Generate NEW Pattern Family
- Call generate_step_pattern_probes(10) with different pattern indices

Step 2: Probe and Evaluate
- Probe all, evaluate top 2

Step 3: Submit best if c2 > 0.8962799441554086

## Key Rules
- USE generate_step_pattern_probes FIRST - never edit the seed directly
- Probe 5-10 patterns before ANY full evaluation
- The pattern space is your primary search space - explore it exhaustively
- Pattern generation is cheap - full evaluation is expensive
