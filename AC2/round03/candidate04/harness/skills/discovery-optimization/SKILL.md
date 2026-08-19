---
name: discovery-optimization
description: "Systematic exploration of C2 function representations with heavy emphasis on step functions (current record), B-splines, and Gaussian mixtures. Uses probe-based ranking to test multiple families before committing eval budget. Reset strategy: when stuck, switch to completely different representation class."
---

# C2 Optimization: Aggressive Family Exploration Playbook

## Current State Analysis
- Seed achieves 1.02649 combined_score (beats world record by ~1.8%)
- Harnesses stalled at 1.02579 - too conservative
- Goal: Break through 1.03+ by exploring families seed neglected

## Key Families to Explore (in priority order)

### 1. STEP FUNCTIONS (Current World Record - Must Test HARDER)
The seed barely tests steps. You MUST explore 5+ step variants:

- Wide support: Support [0.1, 0.9], heights 1.0-2.0
- Asymmetric: Left support [0.05, 0.6], right [0.4, 0.95], different heights
- Multi-level: 4-6 levels with varying heights (e.g., [0.8, 1.2, 1.5, 0.9, 1.3])
- Tapered steps: Steps with linear taper at boundaries
- Optimized heights: Genetic-style height tuning for convolution concentration

Expected: Should match or exceed 0.8963 baseline, potentially reach 0.90+

### 2. B-SPLINES (New Class - Likely Breakthrough)
Seed only uses piecewise-linear. B-splines offer:
- C^k continuity (smoother than sharp steps)
- Local support control
- Flexible shape adjustment

Variants:
- Uniform 100, 200, 300, 500 knots
- Adaptive knots (denser in high-gradient regions)
- Different B-spline orders (linear, quadratic, cubic)

Expected: May concentrate convolution better than steps due to smooth transitions

### 3. GAUSSIAN MIXTURES (Smooth Concentration)
- K=2,4,8,12,20 Gaussians
- Clustered means (tight concentration around center)
- Adaptive variances
- Weight optimization

Expected: Smooth peaks may achieve higher C2 for some formulations

### 4. EXPONENTIAL/RBF FUNCTIONS
- Single exponential: exp(-alpha*|x|)
- Double exponential: exp(-alpha*|x|^beta)
- Radial basis: Gaussian-like with tunable width

Expected: Natural decay, positive everywhere

## Exploration Protocol (20 Evaluations)

### Iterations 1-3: Step Function Deep Dive (3 evals)
1. Call representational_probe to confirm current representation
2. Generate 3 aggressive step variants with probe_solution ranking
3. Evaluate top 2 variants with evaluate_solution

### Iterations 4-6: B-Spline Introduction (3 evals)
1. Call representational_probe (should suggest B-splines if not explored)
2. Test B-spline variants (100, 200, 300 knots) with probes
3. Evaluate top 2 B-spline candidates

### Iterations 7-9: Gaussian Mixtures (3 evals)
1. Call representational_probe
2. Test K=2,4,8 Gaussian mixtures with probes
3. Evaluate top 2

### Iterations 10-12: Exponential/RBF (3 evals)
1. Call representational_probe
2. Test exponential variants with probes
3. Evaluate top 2

### Iterations 13-20: Deep Dive Best Family (7 evals)
- Identify best-performing family from previous rounds
- Increase complexity (more knots/levels/components)
- Use probes to rank 5-10 refined variants
- Evaluate top 3

## Critical Rules

1. Probe before eval: 3-5 probes per family, max 2 evals per family initially
2. Diversify every 4 evals: Never exceed 4 evals on one family before trying new one
3. Step functions are record-holders: Test them MORE than the seed does
4. B-splines are likely breakthrough: Seed barely touched this class
5. Reset when stuck: When same score for 3 evals, call representational_probe and switch families
6. Use all 20 evals: The harness must be aggressive, not conservative

## Tool Usage
- representational_probe: Call at iteration 1 and when score stalls for 2+ evals
- probe_solution: Call 3-5x per family before any eval
- edit_solution: Make ONE complete rewrite per family exploration
- evaluate_solution: Top 2 variants per family only
- finish: When evals exhausted or clear best family identified

## Success Criteria
- Break through 1.03 combined_score
- Identify which function family is most promising
- If possible, reach >0.90 for C2 (seed only achieved ~0.8963)
- Document which variant achieved highest score and why
