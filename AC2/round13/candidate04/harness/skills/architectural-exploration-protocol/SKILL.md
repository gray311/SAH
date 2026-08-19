---
name: architectural-exploration-protocol
description: Diverse architectural exploration with aggressive probe-based filtering and rapid switching.
---

# Architectural Exploration Protocol for C2 Maximization

## Core Principle

The step-function record is a LOCAL OPTIMUM. To beat 0.8962799441554086, you MUST explore DIFFERENT function architectures in PARALLEL, not sequentially refine step functions.

## Phase 1: Diverse Generation (Iterations 1-5)

1. Call generate_candidates to get 3-5 proposals across DIFFERENT families.

2. Families to explore:
   - Gaussian mixtures (smooth, multi-peaked)
   - B-spline basis (flexible smooth transitions)
   - Piecewise-linear (controlled smoothness)
   - Oscillatory with decay (structured convolutions)
   - Multi-level asymmetric steps

3. NEVER start by editing the seed. The seed step patterns are a trap.

## Phase 2: Aggressive Probe Filtering

1. For each proposal, call probe_solution to get approximate scores.

2. You have 30 probes — use them to RANK ALL proposals BEFORE any full evaluation.

3. Select TOP 2-3 by probe score for full evaluation.

4. CRITICAL: If probe score < current best, SKIP full evaluation and try a different proposal.

## Phase 3: Evaluation & Rapid Switching

1. For each top proposal, call evaluate_solution ONCE.

2. If a proposal beats the record: celebrate, but immediately generate NEW candidates from a DIFFERENT family.

3. If NO proposal beats the record after evaluating 3+ candidates: generate a NEW set of candidates from a completely different angle.

## Phase 4: Stalled Recovery (After iteration 10)

- Call generate_candidates again with varied parameters
- Try families you haven't explored yet
- Mix and match: combine elements from successful proposals

## Key Rules

1. PARALLEL EXPLORATION > SEQUENTIAL REFINEMENT
2. PROBE BEFORE EVALUATE — use all 30 probes
3. SWITCH ARCHITECTURES quickly when one fails (within 2-3 iterations)
4. DO NOT spend 5+ iterations on one failed architecture
5. The step-function patterns are a LOCAL OPTIMUM — break out of them immediately
