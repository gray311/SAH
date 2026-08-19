---
name: discovery-optimization
description: "Discover high-C2 functions through radical architectural exploration. The seed's piecewise-linear gradient descent is well-tuned; beat it with completely different representations: Gaussian mixtures, multi-level steps, B-splines, and exponential decays. Use probe_solution to rapidly rank architectural variants and only evaluate top candidates. Never tune parameters of the same representation for 5+ iterations."
---

# C2 Optimization: Radical Architectural Exploration

## Core Principle: Change the Function, Not the Parameters

The seed program achieves ~1.026 with gradient descent on piecewise-linear representations. This is a well-tuned local optimum. To break through, you must discover functions from COMPLETELY DIFFERENT mathematical families.

## Available Function Families

### 1. Gaussian Mixtures (HIGH PRIORITY)
- Form: f(x) = Σ_i w_i * exp(-(x-μ_i)²/(2σ_i²))
- Parameters: K means, variances, weights
- Advantage: Smooth, naturally positive, can concentrate mass effectively

### 2. Multi-Level Step Functions (REFERENCE)
- Current record (0.8963) uses simple step functions
- Try: 3-5 levels with varying heights and widths

### 3. B-Spline Representations
- Use B-spline basis functions with optimized knot positions

### 4. Exponential Combinations
- Form: f(x) = Σ_i w_i * exp(-α_i * |x - μ_i|)
- Parameters: decay rates, centers, weights

## Exploration Protocol

### Phase 1: Rapid Probing
For each NEW function family, generate 10-15 variants using probe_solution:
- Vary: K (2, 3, 5, 10 for mixtures); width ranges; knot placements
- Do NOT tune learning rates or step counts
- Probe 8+ variants before any full evaluation

### Phase 2: Deep Evaluation
Select top 3 from probe rankings. For each:
- Run 2-3 independent seeds with evaluate_solution

### Phase 3: Strategic Reset
- If family A wins: explore deeper within that family
- If NO improvement after 3 evals: switch to a completely different function family

## Critical Rules

1. NEVER tune parameters of the same representation for 5+ iterations
2. probe_solution is your PRIMARY exploration tool
3. First 20 probes should cover 5+ different function families
4. eval budget is precious: max 3 full evals per family
5. The answer likely lies in a representation you haven't tried yet

## Common Pitfalls

- Spending 15 evals optimizing learning rates of piecewise-linear
- Not switching to a different function class when stuck
- Tuning the same representation for too long

## Key Success Factors

- Always use probe_solution to explore new representations
- First exploration should cover 5+ different function families
- The record-breaker is likely in an unexplored family
