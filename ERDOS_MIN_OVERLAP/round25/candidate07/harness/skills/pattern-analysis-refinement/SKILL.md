---
name: pattern-analysis-refinement
description: Two-stage pattern search - generate_ready_candidates for initial patterns, modify_best_pattern for refinement. Evaluate best candidates. Target - analytical c5_bound < 0.37.
---

# Two-Stage Pattern Search for Erdos C5

## Overview
The seed optimizer uses gradient descent but achieves only c5_bound ≈ 0.3809.
We need BETTER structural patterns. Strategy: analytical screening + targeted refinement.

## Stage 1: generate_ready_candidates
Call with temperature=0.5 (or 0.8/1.2 for diversity):
- Returns 3 candidates with integral=1.0 and analytical c5_bound
- Patterns: Golomb ruler, Bipartite, Tri-modal

## Stage 2: modify_best_pattern
Call on the candidate with LOWEST c5_bound from Stage 1:
- Generates 3 variants:
  1. Gaussian smoothing (blurs peaks, may reduce overlap)
  2. Peak sharpening (narrow high regions, concentrate mass)
  3. Phase modulation (sinusoidal interference patterns)
- Each variant has analytical c5_bound computed via FFT

## Evaluation
- Find the best refined candidate (lowest c5_bound)
- If c5_bound < 0.37: CALL evaluate_solution for full test
- If combined_score > 1.0: SUCCESS, call finish

## Temperature Strategy
- Start: temperature=0.5 (standard patterns)
- If no improvement: temperature=0.8 (more varied)
- If still stuck: temperature=1.2 (exploratory)
- Repeat until improvement or budget exhausted

## Expected Outcome
With modify_best_pattern refinement, we should find patterns with
c5_bound < 0.37, beat the seed, and achieve new record bound.
