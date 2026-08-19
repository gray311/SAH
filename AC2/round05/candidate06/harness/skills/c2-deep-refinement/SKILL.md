---
name: c2-deep-refinement
description: Playbook for deeply optimizing piecewise-linear functions before exploring alternatives.
---

# C2 Deep Refinement Playbook

## Objective
Push C2 > 1.02665 by refining the seed's piecewise-linear approach. Do NOT try step functions until you've exhausted refinements.

## Phase 1: Diagnosis
1. Call analyze_convolution once at start
2. Note: discretization_error_estimate, peak_location, tail behavior
3. If error > 0.01: prioritize finer intervals

## Phase 2: Systematic Parameter Search
For EACH parameter group, test 3-5 values:

### Discretization
- num_intervals: [500, 800, 1200, 1600, 2000]
- Probe all 5, pick best, eval top 1

### Learning Rate
- learning_rate: [0.1, 0.15, 0.2, 0.25, 0.3]
- Keep warmup_steps=3000, cosine_decay
- Probe 3, eval best

### Steps
- num_steps: [30000, 50000, 80000]
- Probe all, eval best

## Phase 3: Decision Point
After 3 failed evals with refinements: THEN try step functions.

## Rules
- Probe 3+ variants per parameter before eval
- Call analyze_convolution after each major change
- Do NOT explore new families until current approach fails
- Finer discretization is your first lever
