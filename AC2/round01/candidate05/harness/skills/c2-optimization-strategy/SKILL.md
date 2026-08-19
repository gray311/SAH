---
name: c2-optimization-strategy
description: Playbook for C2 optimization. Structured exploration, multi-scale, probe-before-evaluate.
---

# C2 Optimization

## Objective: Maximize C2
Best: 0.8962799441554086. Target: > 0.8962799441554086.

## Why Structured Over Gradient?
C2 landscape has sharp optima. Gradient descent stuck.

## Phase 1: Coarse Exploration (3-4 evals)
1. 3-5 function classes: piecewise-constant, Gaussian mixtures, Fourier modes, Spline, Exponential
2. 2 variants per class
3. probe all (~15 total)
4. evaluate top 3

## Phase 2: Multi-Scale (3-4 evals)
1. Best from Phase 1
2. Coarse: 15-20 intervals, 1500 steps
3. Fine: 50-60 intervals, 2000 steps, init from coarse
4. evaluate_solution

## Phase 3: Pattern Tuning (2-3 evals)
1. Analyze Phase 2 pattern
2. Variations: shift discontinuities, adjust heights, symmetry
3. Probe to evaluate best

## Phase 4: Final (1-2 evals)
1. Best from Phase 3
2. Fine-tune LR
3. evaluate_solution

## Positivity: f(x) >= 0 via softplus, exp, squaring
## Strategy: probe 10 to evaluate best 2-3

## LR: warmup 500-1000, peak 0.001-0.01, decay cosine to 1e-5
## Patterns: step discontinuities, symmetric, compact support

## Budget: ~20 total. Phase 1: 3, Phase 2: 2, Phase 3: 2, Phase 4: 1-2
