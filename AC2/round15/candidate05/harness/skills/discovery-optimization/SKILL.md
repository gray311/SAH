---
name: discovery-optimization
description: "Parallel diverse exploration protocol. Use probe_and_select to generate diverse function families, then probe_solution to rank before full evaluation. NEVER refine a family that doesn't beat the record on first probe-test."
---

# C₂ Maximizer: Parallel Diverse Exploration Protocol

## Core Principle

Step-function record is a LOCAL optimum. To beat it, explore DIFFERENT function architectures in PARALLEL using probes to filter cheaply.

## Phase 1: Diverse Generation (Iteration 1, every iteration if not improving)

1. Call probe_and_select to get 5-7 proposals across DIFFERENT families:
   - Gaussian mixtures (smooth multi-peaked)
   - B-spline basis (flexible smooth transitions)
   - Piecewise-linear (controlled smoothness)
   - Oscillatory with decay (structured convolutions)
   - Multi-level improved steps (refined asymmetric steps)
   - Convex combinations
   - Exponential-family variations

2. probe_and_select will automatically call probe_solution on each proposal and rank them.

3. EXPECTATION: At least one proposal beats the step-function record on probe.

## Phase 2: Probe-Based Selection

1. Review the ranked proposals from probe_and_select (top 3 by probe score).

2. For each top proposal, call evaluate_solution ONCE to confirm.

3. Track which function FAMILY beats the record.

## Phase 3: Quick Validation or Pivot

1. If ANY proposal beats the record: refine it minimally (one small mutation), then STOP and generate new candidates.

2. If NO proposal beats the record: immediately try a COMPLETELY different set of families.

3. NEVER spend multiple evals on one family unless the first probe-test shows promise.

## Phase 4: Stall Recovery (iteration > 10)

1. Call probe_and_select again with explicitly different families.

2. If still stuck, try combining elements from multiple families.

## Critical Rule

PARALLEL EXPLORATION > SEQUENTIAL REFINEMENT. One probe-test per family. If it fails, abandon it immediately and try a new family.
