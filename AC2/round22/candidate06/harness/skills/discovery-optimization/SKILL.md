---
name: discovery-optimization
description: "Parameter-space refinement for step-function optimization. Extract current best's parameters, generate targeted mutations, use JAX gradients when available. Avoid random family jumps - refine existing architecture first."
---

# C2 Maximizer: Parameter-Space Refinement Protocol

## Core Principle
Step functions have adjustable parameters (interval boundaries, heights, relative widths). Small, guided mutations can escape local optima. DO NOT jump to Gaussian/B-spline families - refine the step architecture first.

## Phase 1: Parameter Extraction + Targeted Mutation (iterations 1-15)

Step 1: Extract Current Best Parameters
- Call analyze_step_parameters on your best function
- Note: interval boundaries, height values, gap sizes, peak position
- If multiple peaks: record each peak's width and relative height

Step 2: Generate Targeted Mutations
Generate EXACTLY 3 variants, each with ONE focused change:

Mutation A (Widen Peak):
- Find the highest peak
- Expand its width by 5% of total domain
- Keep other heights fixed

Mutation B (Redistribute Heights):
- Find tallest and shortest heights
- Increase tallest by 0.1, decrease shortest by 0.1
- Ensure all heights > 0

Mutation C (Shift Peak):
- Shift the peak center by 5% of domain (left or right randomly)
- Keep shape constant

Step 3: Probe and Evaluate
- Call probe_solution on ALL 3 variants (3 probes total)
- Rank by probe score
- Call evaluate_solution on TOP 1 only
- If probe score < 1.0: skip full eval and try Mutation A with opposite direction

Step 4: Iterate
- If beats record: continue with refined parameters
- If no improvement after 3 iterations: switch to Phase 2

## Phase 2: Gradient-Based Refinement (iterations 16-25)

Step 1: Compute Gradients
- Use JAX autodiff: @jax.jit @jax.grad on the objective function
- Compute gradient w.r.t. each parameter (interval start, end, height)

Step 2: Gradient Ascent Step
- Take gradient step: new_param = param + learning_rate * gradient
- Use learning_rate = 0.05 initially, decay to 0.01
- Clip parameters to valid range

Step 3: Variants from Gradients
Generate 2 variants:
- Variant 1: Follow positive gradient direction
- Variant 2: Follow negative gradient direction (descent, to explore local structure)

Step 4: Probe and Evaluate
- Probe both, evaluate best
- If gradient norm < 0.001: switch to Phase 3

## Phase 3: Aggressive Reinitialization (iterations 26-30)

Step 1: Preserve Best Features
- Keep the highest peak height and its position
- Reinitialize all other parameters with noise (std = 0.1 * parameter value)

Step 2: Generate 2 Reinitializations
- Reinit 1: Keep best peak, randomize others
- Reinit 2: Try 2-peak configuration (split best peak)

Step 3: Final Evaluation
- Probe both, evaluate best
- Submit if c2 > 0.8962799441554086

## Key Rules
- NO random family generation - refine step parameters only
- Use probes to filter: 5-6 probes before any full eval
- Call analyze_step_parameters EVERY iteration
- If iteration 15+ with no improvement: try gradient ascent (Phase 2)
- Learning rate schedule: 0.05 → 0.01 → 0.005 (decay as you converge)
