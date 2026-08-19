---
name: discovery-optimization
description: "Iteratively optimize a program's EVOLVE-BLOCK to maximize C2 for the second autocorrelation inequality. The seed uses piecewise-linear but record-breakers are piecewise-constant (step functions). Use structural_probe to discover this, then aggressively test step variants with probe_solution. Diversify function representations instead of tuning hyperparameters."
---

# C2 Representation Switching Playbook
## Core Principle: Switch Representations Early
The seed program uses piecewise-linear representation. Record-breakers at 0.8963 use piecewise-constant (step functions). Do NOT spend 20 evals tuning piecewise-linear hyperparameters. Call structural_probe to detect your class, and SWITCH if you are not using step functions.
## Protocol: Detect, Switch, Explore
### Phase 1: Initial Detection (Call structural_probe)
1. Call structural_probe at iteration 0 2. It will report: detected_class, params_count, and CRITICAL recommendation 3. If recommended to switch: IMMEDIATELY edit to use step functions
### Phase 2: Immediate Switch if Needed
If structural_probe says piecewise-linear or recommends switching:
Edit your code to use step functions: Replace piecewise-linear initialization with step functions using: f = jnp.zeros(n) start = int(0.25 * n) end = int(0.75 * n) h = 1.0 f = f.at[start:end].set(h)
Test these step variants (use probe_solution): 1. Symmetric step: start=0.25n, end=0.75n, h=1.0 2. Wide step: start=0.2n, end=0.8n, h=0.9 3. Narrow step: start=0.3n, end=0.6n, h=1.3 4. Asymmetric left: start=0.15n, end=0.55n, h=1.15 5. Multi-level: 2-3 different heights in different regions
### Phase 3: Probe-Based Ranking
For step functions (and any new representation): - Test 10+ variants with probe_solution - Use DIFFERENT step widths, heights, supports - Probe, don't eval yet (save your 20 evals!)
### Phase 4: Full Evaluation
Only after probing: 1. Select top 3 candidates from probe scores 2. Each: 2-3 random seeds with evaluate_solution 3. Track which representation class wins
### Phase 5: Deep Dive or Reset
- If step functions win: increase intervals, try more step patterns - If piecewise-linear wins: DON'T TUNE - switch to Gaussian mixtures or B-splines - If no improvement after 5 evals: call structural_probe and SWITCH to a completely different family
## Critical Rules
1. Call structural_probe at iteration 0 - Don't waste iterations guessing 2. Switch immediately if recommended - A one-line change to step functions 3. Test 10+ probes per representation - Don't eval early 4. Max 5 evals per family - Diversify! 5. Step functions are your friend - They beat piecewise-linear at 0.8963
## Avoid These Pitfalls
- Spending 10+ iterations tuning piecewise-linear hyperparameters - Ignoring structural_probe recommendations - Evaluating before probing - Not testing enough step function variants - Assuming smooth functions (Gaussian, spline) will win over steps
