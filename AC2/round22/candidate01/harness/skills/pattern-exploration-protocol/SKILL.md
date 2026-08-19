---
name: pattern-exploration-protocol
description: Systematic step-pattern generation and probe ranking. Generate patterns, rank with probes, evaluate best.
---

# C2 Maximizer: Pattern Exploration Protocol

## Core Principle
Generate diverse step patterns using generate_step_pattern_probes, then RANK THEM ALL with probe_solution before any full evaluation. The pattern space is your primary search space.

## Phase 1: Pattern Generation and Probe Ranking (iterations 1-10)

Step 1: Generate Pattern Pool
- Call generate_step_pattern_probes(10) to generate 10 diverse patterns
- These are ready-to-evaluate step functions with different heights and widths

Step 2: Probe All Patterns
- Call probe_solution on ALL 10 generated patterns (10 probes)
- Rank by probe score (higher C2 is better)

Step 3: Full Evaluation
- Call evaluate_solution on TOP 2 by probe score
- If either beats record: switch to Phase 2 with best pattern

Step 4: Iterate
- If no improvement after 3 iterations: expand pattern diversity

## Phase 2: Parameter Refinement (iterations 11-20)

Step 1: Generate Refined Patterns
- Call generate_step_pattern_probes(5) with refinements
- Variations: adjust peak heights by +/-0.1, expand/contract width by 5%

Step 2: Probe and Evaluate
- Probe all 5, evaluate best

Step 3: Continue Until Budget Exhaustion

## Phase 3: Aggressive Re-Exploration (iterations 21-30)

Step 1: Generate NEW Pattern Family
- Call generate_step_pattern_probes(10) with different pattern indices

Step 2: Probe and Evaluate
- Probe all, evaluate top 2

Step 3: Submit best if c2 > 0.8962799441554086

## Key Rules
- USE generate_step_pattern_probes FIRST - never edit seed directly
- Probe 5-10 patterns before ANY full evaluation
- The pattern space is richer than the seed - explore it exhaustively
