---
name: c2-systematic-exploration
description: A method playbook for discovering high-C2 functions through systematic representation exploration. Uses probe-based ranking to test multiple function families before committing evaluation budget. Emphasizes diversification over deep tuning of a single representation.
---

# C2 Systematic Exploration Playbook

## Core Insight
The search for better C2 values is dominated by FUNCTION REPRESENTATION, not hyperparameter tuning. The current record (0.8963) is achieved by step functions. Your harness must systematically explore multiple representations.

## Exploration Protocol

### Step 1: Initial Probe (Call representational_probe)
- Understand what function class your current code implements
- Get recommendations for alternatives
- If you are on piecewise-linear, immediately test step functions

### Step 2: Probe-Based Family Exploration
For EACH of these function families, test 8-10 variants using probe_solution BEFORE any full evaluation:

#### Family A: Piecewise-Constant (Step Functions)
- 3 variants: narrow steps (0.1n), wide steps (0.5n), multi-level (3 heights)
- Expected: Should match or beat 0.8963 baseline

#### Family B: Piecewise-Linear (Current Seed)
- 4 variants: intervals=100, 200, 500; triangular peak; trapezoid
- Expected: Test if smoothness helps

#### Family C: Gaussian Mixtures
- 4 variants: K=2,3,5,10; equal variance; clustered means
- Expected: Smooth concentration may improve C2

#### Family D: B-Splines
- 2 variants: uniform knots, adaptive knots
- Expected: Test local support benefits

#### Family E: Exponential Combinations
- 2 variants: single exponential, double exponential
- Expected: Natural decay behavior

### Step 3: Full Evaluation (Limited Budget)
- Select top 3 candidates from probe scores
- Each: 2-3 random seeds with evaluate_solution
- Track: which family performs best

### Step 4: Deep Dive or Reset
- If top family shows promise: increase budget (more intervals, more steps)
- If NO improvement after 5 evals: RESET with a completely different family
- NEVER spend more than 5 evals on the same family without trying something new

## Key Rules
1. Probe before eval: 8+ probes per family, max 3-5 evals
2. Diversify early: First exploration should cover 4+ families
3. Reset strategy: When stuck, switch function families, don't tune same one
4. Record scores: Track which family, which variant achieved what

## Avoid These Pitfalls
- Tuning hyperparameters of a single representation for 10+ iterations
- Spending all 20 evals on piecewise-linear before trying steps
- Ignoring that step functions (0.8963) are the current record - test them!
- Not using probes - they are your primary exploration tool
- Overthinking: 3-5 good evals are enough; diversify more than optimize
