---
name: diverse-exploration-protocol
description: Parallel exploration across function families with probe-based filtering.
---

# Diverse Exploration Protocol for C2 Maximization

## Core Principle

The step-function record is a LOCAL optimum. To beat it, you MUST explore DIFFERENT function
architectures in PARALLEL, not sequentially refine one type.

## Phase 1: Diverse Generation (Iteration 1)

1. Call generate_candidates to get 3-5 proposals across DIFFERENT families.

2. Families to explore:
   - Gaussian mixtures (smooth, multi-peaked)
   - B-spline basis (flexible smooth transitions)
   - Piecewise-linear (controlled smoothness)
   - Oscillatory with decay (structured convolutions)
   - Improved multi-level steps

3. EXPECTATION: At least one family should beat the step-function record.

## Phase 2: Probe-Based Filtering

1. For each proposal, call probe_solution to get approximate scores.

2. You have 30 probes - use them to RANK all proposals BEFORE spending full evaluations.

3. Select top 3-5 by probe score for full evaluation.

4. If a probe score is < current best, SKIP full evaluation and try a different proposal.

## Phase 3: Full Evaluation & Refinement

1. For each top proposal, call evaluate_solution ONCE to confirm.

2. If a proposal beats the record: refine it slightly (small mutations), but DON'T exhaust it.

3. If no proposal beats the record: generate a NEW set of candidates from a different angle.

## Phase 4: Stalled Recovery

If stuck after 10 iterations:
- Call generate_candidates again
- Try completely new families (e.g., if only tried smooth functions, try sharp ones)
- Mix and match: combine elements from successful proposals

## Key Rule

PARALLEL EXPLORATION > SEQUENTIAL REFINEMENT. When one type fails, immediately switch to a new type.
Do not spend 5+ iterations refining a function family that is not beating the record.
