---
name: discovery-optimization
description: "Explore multiple function families (steps, splines, hybrids) with structural diversity. Probe 2-3 variants per family, evaluate 1-2 top candidates. Maximize C2 > 1.03. Use step_config_generator for steps, but also try splines and hybrids. Temperature=1.1 for exploration."
---

# Step Function Optimization for C2 Maximization

## Objective
Maximize C2 = ||f * f||_2^2 / ((int_f)^2 ||f * f||_inf). Current baseline: 1.026. Target: > 1.026.

## Why Step Functions?
- Theoretical record holders at 0.8963
- Simple: piecewise-constant (not linear!)
- Easy to parameterize with step_config_generator

## Workflow

### Step 1: Get Configuration
CALL step_config_generator FIRST to get:
- intervals: list of (start, end, height)
- num_steps: number of step regions
- params: heights, widths, symmetry

### Step 2: Create TRUE Step Function
Use edit_solution with step_config_generator output to create TRUE piecewise-constant function:
- Use jnp.piecewise or jnp.where
- Specify exact intervals and heights
- NOT linear ramps - must be constant over intervals

### Step 3: Probe & Rank
- Call probe_solution on 3-5 step variants
- Rank by probe score
- Only evaluate TOP 2

### Step 4: Diversify Configurations
Try different configurations:
- Symmetric vs asymmetric
- 2-step, 3-step, 4-step
- Different heights: 1.0, 1.5, 1.2, 1.0, 1.3, etc.

## Critical Rules
- MAX 4 full evaluations
- ALWAYS use step_config_generator first
- Probe 3-5 before any eval
- Edit to create TRUE step functions (constant, not linear)
- finish when done
