---
name: discovery-optimization
description: "Parallel multi-family exploration with probe-driven filtering. Generate diverse candidates from Gaussian mixtures, B-splines, oscillatory, piecewise-linear, and improved step families. Probe all, evaluate top 3, refine slightly only if beating record."
---

# C₂ Maximizer: Parallel Multi-Family Exploration

## Core Principle
Step functions are a LOCAL optimum. To beat C₂ = 0.8962799441554086, you MUST explore DIFFERENT function families IN PARALLEL, not sequentially refine one type.

## Workflow (Repeatable Every 5-10 Iterations)

### Step 1: Diverse Generation
Call generate_candidates to get 3-5 proposals from DIFFERENT families:
- Gaussian mixtures: f(x) = Σ w_i · exp(-((x-μ_i)²)/(2σ_i²))
- B-spline basis: 30-50 control points with softplus positivity
- Oscillatory decay: f(x) = (1 + α cos(βx)) · exp(-γ|x|)
- Piecewise-linear: vertices with optimized heights
- Multi-level improved steps: asymmetric step patterns

### Step 2: Probe All Candidates
You have 30 probes total. PROBE EVERY candidate from Step 1 before any full evaluation.
- Rank candidates by probe score
- Discard any with probe score < current best (1.04199)

### Step 3: Evaluate Top 3
Select top 3 by probe score. Call evaluate_solution ONCE per candidate.
- If ANY beat 1.04199: great! Go to Step 4
- If NONE beat the record: Go to Step 5

### Step 4: Slight Refinement (Only if beating record)
If a candidate beats the record:
- Apply ONE tiny mutation (±0.02 height, ±2% width)
- Probe the refined version
- If still better: evaluate it
- Then return to Step 1 for fresh exploration

### Step 5: Stalled Recovery (No improvement)
If no candidate beats the record:
- Generate a NEW set from different families
- Try hybrid ideas: e.g., "Gaussian-like with step edges", "oscillatory steps"
- Vary the parameter ranges: wider oscillations, different decay rates

## Key Rules
- PARALLEL EXPLORATION > SEQUENTIAL REFINEMENT
- Probe ALL before evaluating ANY
- Never refine the same family >2 iterations without trying new families
- After 5 iterations with no improvement: generate completely new ideas
- Use JAX mutability: f = f.at[start:end].set(value)
