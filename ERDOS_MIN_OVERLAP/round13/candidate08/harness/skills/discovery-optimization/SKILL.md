---
name: discovery-optimization
description: "Create constraint-satisfying initializations to start optimization from feasible points, then screen with probes."
---

# Constraint-Satisfying Initialization Strategy

## The Problem

All 12 seed patterns use sigmoid(latent) but don't guarantee integral(h)=1.
They start from INFEASIBLE points, wasting optimizer steps.

## The Solution

Use constraint_satisfying_init to create latents where:
- h = sigmoid(latent)
- integral(h) = 1 (exactly)

This means starting from FEASIBLE points.

## Workflow

1. CALL constraint_satisfying_init (returns 4 latents with integral(h)=1)
2. For each latent, EDIT seed to use ONLY that pattern:
   - num_restarts=1
   - seed_start = pattern index
   - Or better: replace _get_best_initialization with a single-pattern version
3. Call probe_solution to check c5_bound (integral is already 1!)
4. Call evaluate_solution on top 1-2 with c5_bound < 0.37
5. If no success, ADD a piecewise constant pattern (not sigmoid, just step values)
   that can be scaled to have integral=1

## Why This Works

- Start from FEASIBLE points, not infeasible ones
- Optimizer spends all steps improving c5_bound, not fixing constraints
- FFT evaluator is fast enough for 3-5 full evaluations
- Piecewise constant patterns (not sigmoid) can directly encode step functions
