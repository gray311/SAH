---
name: discovery-optimization
description: "Systematically perturb the seed program using mutation_probe to explore function representations.\nProbe 5+ variants per family before evaluating. Diversify after 3 stale probes. Maximize C2 > 1.026."
---

# C2 Optimization: Systematic Mutation Protocol

## Objective
Maximize C2 = ||f * f||₂² / ((∫f)² ||f * f||_∞). Current baseline: 1.026. Target: > 1.026.

## Core Principle: Mutation-Based Exploration
Don't guess mutations - use mutation_probe to generate systematic variants. For each function family, probe 5+ variants before any full evaluation.

## Phase 1: Initial Analysis
1. Call mutation_probe immediately to detect current function class
2. Examine the returned mutations (step_width, step_height, num_pieces, etc.)
3. If not exploring step functions (record holders at 0.8963), prioritize them

## Phase 2: Probe-Based Family Exploration
For EACH function family, test 5-10 variants using mutation_probe + probe_solution:

### Family A: Piecewise-Linear (Seed)
- Mutations: num_intervals = [100, 200, 400, 800], reinit_fraction = [0.05, 0.1, 0.2], reinit_std = [0.01, 0.02, 0.05]
- Expected: Test if more intervals or different reinit strategies help

### Family B: Piecewise-Constant (Step Functions)
- Mutations: step_width = [0.1n, 0.25n, 0.5n], num_pieces = [2, 3, 5], heights = [1.0, 1.2, 1.5]
- Try: symmetric, asymmetric, multi-level steps
- Expected: Should match or beat 0.8963 theoretical baseline

### Family C: Gaussian Mixtures
- Mutations: K = [2, 3, 5], sigma = [0.1, 0.2, 0.5], means = [uniform, clustered]
- Ensure: non-negative (use softplus)

### Family D: B-Splines
- Mutations: num_knots = [5, 10, 20], knot_spacing = [uniform, adaptive]

### Family E: Exponential Combinations
- Mutations: decay_rates = [0.1, 0.2, 0.5], num_terms = [1, 2]

## Phase 3: Full Evaluation
1. Select top 3 candidates from probe scores
2. Each: run with 2 random seeds using evaluate_solution
3. Track: which family performs best

## Phase 4: Deep Dive or Reset
- If top family: increase budget (more intervals, finer steps)
- If NO improvement after 4 evals: call mutation_probe and SWITCH mutation type

## Critical Success Factors
- Probe before eval: 5+ probes per family, max 3-4 evals
- Use mutation_probe to generate concrete mutations (not vague suggestions)
- Diversify early: Cover 3+ families within first 15 probes
- Reset strategy: When stuck, switch mutation types, don't tune same one
- Record scores: Track which family, which mutation achieved what
## Tool Usage Priority
1. mutation_probe — generate systematic mutations for current family
2. probe_solution — rank many variants cheaply
3. edit_solution — apply top mutation from probe results
4. evaluate_solution — confirm only 2-3 top candidates
5. finish — when evals exhausted or score > 1.026 achieved
