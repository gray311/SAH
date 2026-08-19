---
name: structured-search-playbook
description: Guide the solver to use diverse structural initializations instead of hyperparameter sweeps. Call generate_erdos_constructs to get fundamentally different function shapes, optimize each briefly, and evaluate. Iterate with new constructions when stuck.
---

# Structured Search Playbook for Erdos Minimum Overlap

## Core Principle: Structure Beats Parameters

The Erdos problem's optimal solutions have specific structural properties that random
or parametric variations don't discover. You must GENERATE new structures, not just tune
existing ones.

## Method: Diverse Structural Search

### Step 1: Generate Diverse Constructions
Call generate_erdos_constructs() to get 5-6 structurally different initializations:
- Each has a fundamentally different "shape"
- Examples: bimodal, Golomb-based, finite-field, alternating patterns
- These are designed to break out of standard local minima

### Step 2: Short-Focus Optimization
For each construction:
- Set num_intervals=400 (fast iteration)
- Set num_steps=2000-3000 (quick convergence attempt)
- Set num_restarts=1 (focused search)
- Set base_learning_rate=0.01 (good exploration)
- Set penalty_strength=100-500 (reasonable constraint enforcement)

### Step 3: Quick Screening
Call probe_solution for each variant to:
- Check if constraint (∫h=1) is approximately satisfied
- Get rough quality estimate
- Skip variants that clearly fail constraints

### Step 4: Full Evaluation
For variants that pass screening:
- Call evaluate_solution for full score
- Record the best combined_score

### Step 5: Refinement Loop
After testing all constructions:
- Pick the best-scoring variant
- Call generate_erdos_constructs() again for NEW constructions
- Optionally refine the best variant:
  * Increase num_intervals to 800 for finer resolution
  * Increase num_steps to 10000 for better convergence
  * Add small noise to break out of new local minima
- Continue until combined_score > 1.0 or budget exhausted

## When to Use This Strategy

- ALWAYS at the start: you have no good structure
- WHEN STUCK: if your score hasn't improved for 5+ iterations
- BEFORE GIVING UP: try one more batch of diverse constructions

## What Makes This Different From Hyperparameter Sweeps

- Hyperparameter sweeps: same structure, different parameters (low-dimensional search)
- Structured search: different structures entirely (high-dimensional, diverse search)
- The problem needs structural innovation, not parameter tuning
