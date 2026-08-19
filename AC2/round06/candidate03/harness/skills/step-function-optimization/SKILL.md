---
name: step-function-optimization
description: Method playbook for C2 optimization using step functions (theoretical champions at 0.8963). Focus on diverse step configurations, probe before eval, maximum 4 evals.
---

# Step Function Optimization for C2 Maximization

## Objective
Maximize C2 > 1.026. Current baseline: 1.026 (seed). Theoretical best: 0.8963 (step functions).

## Why Step Functions?
- Proven record holders in this task
- Simple structure: constant over intervals
- Easy to parameterize: intervals, heights, symmetry

## Strategy: Systematic Step Exploration

### Phase 1: Symmetric Step Functions
1. Create 2-step: f(x) = height for |x| < width, 0 otherwise
2. Create 3-step: left < right < center > left
3. Create 4-step: bimodal with valley in center
4. Vary heights: [1.0, 1.5], [1.2, 1.0, 1.3], [1.5, 1.2, 1.5]

### Phase 2: Asymmetric Step Functions
1. Shifted single peak: all mass on one side
2. Multi-cluster: three separate peaks
3. Skewed: wider on one side

### Phase 3: Hybrid Approaches
1. Step + small polynomial tail
2. Step with smooth transitions

## Probe-Before-Eval Protocol
1. Generate 5-8 step configurations (vary intervals, heights, symmetry)
2. Probe each (call probe_solution)
3. Rank by probe score
4. Evaluate TOP 2-3 only

## If No Progress
- Try polynomial decay: f(x) = exp(-alpha * |x|^beta)
- Try Gaussian mixtures: sum of Gaussians with varied sigmas
- Try the seed's multi-start optimization with different initializations

## Critical Rules
- MAX 4 full evaluations
- Always probe 5+ variants before any eval
- Diversify: try symmetric, then asymmetric, then hybrid
- Use step_config_generator tool for structured exploration
