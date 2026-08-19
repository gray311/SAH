---
name: break-local-optima-strategy
description: A method playbook for escaping the piecewise-linear local optimum and discovering novel high-C₂ functions through structural changes.
---

# Escaping Local Optima in C₂ Optimization

## The Core Problem

The seed program uses piecewise-linear optimization with 300 intervals. It has converged to a local optimum (~0.8963). **Do not try to improve this configuration further.** Your job is to replace the function representation entirely.

## The Strategy: Structural Innovation Over Parameter Tuning

### Step 1: Detect Current Representation
Use function_class_detector to identify what function class the current code uses.
- If it's piecewise-linear (the seed): STOP. This class is exhausted.
- If it's already something else: Great! You're on the right track.

### Step 2: Choose a NEW Representation Class
Pick a class the seed has NOT explored:

**A. Step Functions (Piecewise-Constant)**
- Why: Historical record holder (0.8963), simple, interpretable
- Implementation: Replace _create_initializer to return flat regions
- Parameters: Number of steps (2-5), support width, heights
- Probe variations: 5 different step patterns

**B. Gaussian Mixtures**
- Why: Smooth, convex-like, often optimal for integral problems
- Implementation: f(x) = Σ w_i * exp(-(x-μ_i)²/(2σ_i²))
- Parameters: K means, K variances, K weights
- Probe variations: K=2, K=3, K=5 with different spreads

**C. Exponential Combinations**
- Why: Simple decay, always positive, fewer parameters
- Implementation: f(x) = Σ w_i * exp(-α_i * |x - μ_i|)
- Parameters: K centers, K decay rates, K weights
- Probe variations: Single exponential, double exponential

### Step 3: Rapid Probe Screening
For each new representation:
1. Create 3-5 variant implementations
2. Score all with probe_solution (fast, ~10s each)
3. Pick the top 1-2 by probe score
4. If top probe score > seed score, spend 1 full evaluation
5. If all probes < seed, abandon this class and try another

### Step 4: Refinement (Only After Beating Seed on Probes)
For the winning representation:
- Increase intervals by 2-3x
- Use multi-start (5 different initializations)
- Fine-tune hyperparameters (learning rate, steps)
- This is where you might finally beat 0.8963

## Common Mistakes to Avoid

❌ Spending multiple evaluations on piecewise-linear parameter tuning
❌ Trying 10+ parameter variations of the same representation
❌ Not trying at least 3 different function classes
❌ Ignoring probe scores and jumping to full evaluations
✅ **DO**: Try step functions FIRST (historical precedent)
✅ **DO**: Use probes to screen 10+ representations quickly
✅ **DO**: Only invest full evals in representations that beat seed on probes
✅ **DO**: Switch function classes immediately if stuck
