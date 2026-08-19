---
name: constructive-c5-strategy
description: Constructive approach for C₅ bound. Generate diverse step functions, not random gradient descent starts.
---

# Constructive C₅ Optimization Strategy

## Problem
Find h:[0,2]→[0,1] minimizing max_k ∫ h(x)(1-h(x+k))dx, subject to ∫h=1.
Current best: C₅ ≤ 0.38092303510845016

## Success Strategy: CONSTRUCT FIRST, Optimize SECOND

### Phase 1: Generate Diverse Constructions

Use construct_step_functions with n_candidates=30, max_intervals=5-10.

### Phase 2: Probe and Filter

Call probe_solution for each candidate. Keep top 3-5.

### Phase 3: Full Evaluation

Call evaluate_solution on the best candidates.

### Key Insight

Start simple (few intervals) with mathematically-informed constructions.
