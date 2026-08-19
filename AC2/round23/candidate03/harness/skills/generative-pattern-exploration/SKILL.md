---
name: generative-pattern-exploration
description: Generate diverse multi-level step-function patterns from scratch. Explore multi-modal, asymmetric, and high-complexity configurations. Use probes aggressively to screen variants.
---

# C2 Maximizer: Generative Pattern Exploration Protocol

## Core Principle

Generate COMPLETE new step-function patterns from scratch. The seed found one local optimum - you need to discover NEW function classes.

## Phase 1: Generative Exploration (iterations 1-18)

Step 1: Call generate_step_pattern

Generate patterns across these categories:

Category A - Multi-Level Peaks (2-5 levels):
- 3 levels: low-high-low, low-high-medium-low
- 4 levels: staircase, asymmetric pyramid
- 5 levels: complex multi-modal

Category B - Asymmetric Patterns:
- Narrow peak (10-20% width) with wide low base (80-90%)
- Wide base (60-80%) with medium peak (20-30%)
- Staircase: monotonically increasing/decreasing steps

Category C - Multi-Modal (2-3 distinct peaks):
- Two peaks with valley in between
- Three peaks with two valleys
- Each peak: unique width (5-15%) and height (1.0-2.5)

Step 2: Diversity Parameters

- num_levels: 2-5 (start simple, increase if stuck)
- peak_positions: 2-5 fractional positions (0.1-0.9)
- heights: 0.5-3.0 (ensure positive)
- base_width: 0.3-0.7 (fraction of domain)

Step 3: Probe-First Strategy

- Call probe_solution on ALL generated variants (10 probes max per iteration)
- Rank by probe score
- Call evaluate_solution on TOP 2 only (if probe >= 1.0)

Step 4: Iterate from Best

- Use best pattern as inspiration for next generation
- If no improvement: increase num_levels, try new category

## Phase 2: High-Resolution Refinement (iterations 19-25)

- Same pattern structure but 2x num_intervals
- Probe 3, evaluate best

## Phase 3: Aggressive Diversification (iterations 26-30)

Try new families:
- Gaussian-step hybrids (higher center, smoother edges)
- Exponential-step hybrids (decay from peak)
- 3+ peak multi-modal

## Key Rules

- GENERATE complete patterns from scratch
- USE PROBS AGGRESSIVELY (30 available!)
- If stuck: increase complexity, try new families
- NEVER rely on parsing/editing - generate new patterns
