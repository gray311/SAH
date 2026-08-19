---
name: discovery-optimization
description: "Two-stage pattern search: generate_ready_candidates for initial patterns (analytical\nscreening), modify_best_pattern for structural refinement. Evaluate best candidates.\nTemperature controls pattern diversity. Target: analytical c5_bound < 0.37."
---

# Two-Stage Pattern Search for Erdos C5

## Why This Strategy
The seed optimizer uses 59000-step gradient descent with 3 restarts, achieving
only c5_bound ≈ 0.3809 (combined_score=0.999945). The problem needs BETTER
structural patterns, not more optimization iterations.

## Stage 1: generate_ready_candidates (INHERITED TOOL)
Call with temperature=0.5:
- Returns 3 candidates with integral=1.0 by construction
- Each has analytical c5_bound computed via FFT (exact, no training)
- Patterns: Golomb ruler, Bipartite, Tri-modal

## Stage 2: modify_best_pattern (NEW TOOL - See tool_descriptions)
Call on the candidate with LOWEST c5_bound from Stage 1:
- Generates 3 refined variants:
  1. Gaussian smoothing: convolves with Gaussian kernel
  2. Peak sharpening: amplifies high regions
  3. Phase modulation: sinusoidal interference
- Each variant has analytical c5_bound computed via FFT

## Evaluation
- Find the best refined candidate (lowest c5_bound)
- If c5_bound < 0.37: CALL evaluate_solution for full test
- If combined_score > 1.0: SUCCESS, call finish

## Temperature Strategy
- Start: temperature=0.5 (standard patterns)
- If no improvement: temperature=0.8 (more varied)
- If still stuck: temperature=1.2 (exploratory)

## Budget Use
- 60 eval budget total
- Per iteration: 1 generate_ready_candidates + 1 evaluate_solution + 1 modify_best_pattern
- Expect 10-15 iterations to find improvement

## Expected Outcome
With modify_best_pattern refinement, we should find patterns with
c5_bound < 0.37, beat the seed, and achieve new record bound.
