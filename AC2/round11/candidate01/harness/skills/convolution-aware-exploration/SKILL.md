---
name: convolution-aware-exploration
description: Convolution-aware exploration for C₂ maximization. Use analyze_convolution to diagnose current patterns, generate targeted mutations, probe multiple variants, and iterate. Always probe before full evaluation; use compare_variants to rank before committing evals.
---

# Convolution-Aware C₂ Exploration

## Overview

The seed's step patterns are locally optimized. You need CONVOLUTION-AWARE exploration:
understand the current best's convolution structure, then target its weaknesses.

## Phase 1: Diagnostic Analysis

1. Call analyze_convolution on the current best pattern
2. Note: peak location, peak_fraction, L2 concentration
3. If peak_fraction > 0.2: L_inf is dominated by one peak → try adding side peaks
4. If l2_concentration > 1.5: L2 too concentrated → try widening support

## Phase 2: Targeted Generation

Based on analysis:

**If L_inf peak too dominant:**
- Add asymmetric side peaks: [0.4h, 1.6h, 0.5h, 1.4h, 0.3h]
- Use smooth transitions between steps
- Try irregular spacing to avoid constructive interference

**If L2 too low:**
- Widen the support (extend tails)
- Add secondary peaks at optimal distances
- Try exponential decay tails

**If symmetric:**
- Try asymmetric multi-peaked patterns
- Try irregular interval placements

## Phase 3: Probe-First Evaluation

1. Generate 3-5 variants targeting identified weaknesses
2. Call probe_solution on ALL (cheap ranking)
3. Call compare_variants to rank by heuristic C₂
4. Call evaluate_solution ONLY on top 1 variant
5. If failed: call analyze_convolution to diagnose

## Phase 4: Iteration

- When variant improves: analyze WHY (use analyze_convolution on new best)
- Generate more variants in successful pattern class
- If stuck: try completely different function class (smooth, exponential, spline)

## Key Principles

- ANALYZE first: understand convolution structure before mutating
- PROBE all: rank variants cheaply before full evals
- COMPARE: use compare_variants to narrow down before evaluate
- TARGETED: use analysis insights to guide mutations
- DIVERSE: if stuck, explore different function classes
