---
name: discovery-optimization
description: "Step function optimization for C2 maximization. Analyze current best with analyze_step_config, generate diverse configs with step_config_generator, probe 3-5, evaluate top 2. Use iterative refinement guided by analysis. Maximize C2 > 1.026."
---

# Step Function Optimization for C2 Maximization

## Objective

Maximize C2 = ||f * f||_2^2 / ((int_f)^2 ||f * f||_inf). Current baseline: 1.026. Target: > 1.026.

## Why Step Functions?

- Theoretical record holders at 0.8963
- Simple: piecewise-constant (not linear!)
- Easy to parameterize with step_config_generator and analyze_step_config

## Workflow

### Step 1: Analyze Current Best

CALL analyze_step_config FIRST to understand the current best function:

- Extract the step parameters (intervals, heights, widths)
- Identify the current peak height, plateau widths
- Get suggestions for improvements:
  * "INCREASE_PEAK_HEIGHT": Try higher plateau (1.5 → 1.8 → 2.0)
  * "WIDEN_PLATEAU": Expand central region
  * "NARROW_PLATEAU": Tighten central peak
  * "ADD_WINGS": Add outer asymmetric steps
  * "SHARPEN_EDGES": Make transitions steeper

### Step 2: Generate Variants

Use step_config_generator to create NEW configurations:

- Call with different num_steps (3-8)
- Vary symmetric vs asymmetric
- Try different peak_positions

### Step 3: Create TRUE Step Function

Use edit_solution with parameters from either:
- analyze_step_config suggestions (for iterative refinement)
- step_config_generator output (for exploration)

CRITICAL: Create piecewise-CONSTANT functions (flat over intervals), NOT linear ramps!

### Step 4: Probe & Rank

- Call probe_solution on 3-5 step variants
- Rank by probe score
- Only evaluate TOP 2

### Step 5: Iterative Refinement

- After each full evaluation, CALL analyze_step_config on the NEW best
- Use its suggestions to guide next iteration
- Continue until no improvement or budget exhausted

## Common Improvement Patterns

1. Peak height: 1.0 → 1.3 → 1.6 → 1.9 (increase systematically)
2. Plateau width: narrow → wide → very wide (test both)
3. Asymmetry: Try centered peak, then offset to left/right
4. Multi-peak: After single peak, try 2-peak, then 3-peak configurations

## Critical Rules

- ALWAYS start with analyze_step_config to understand current best
- Probe 3-5 before any evaluate (max ~4 total evals)
- Use analyze_step_config after each eval to guide refinement
- Edit to create TRUE step functions (constant, not linear)
- finish when no improvement after 2-3 refinement cycles or budget exhausted
