---
name: discovery-optimization
description: "Ratio-aware refinement for step-function optimization. Extract interval/height ratios, analyze structure, generate targeted mutations. Use analyze_ratio_structure to understand current best before mutating."
---

# C2 Maximizer: Ratio-Aware Refinement Protocol
## Core Principle
Step function performance depends on ratio properties: interval width ratios and height-to-width ratios. Analyze these ratios before mutating - theoretical optimality suggests certain ratio patterns.
## Phase 1: Ratio-Structure Exploration (iterations 1-12)
Step 1: Analyze Ratio Structure
- Call analyze_ratio_structure ONCE per iteration
- This tool extracts: interval widths, height values, width ratios, height ratios
Step 2: Generate Ratio-Guided Mutations
Generate EXACTLY 3 variants:
Mutation A (Narrow Tall Peaks):
- Find the narrowest interval with height > 1.3
- Narrow it by 10% and increase height by 0.1
- Rationale: Narrow tall peaks concentrate convolution mass
Mutation B (Widen Valleys):
- Find a valley (low-height interval between peaks)
- Widen it by 15% and decrease height by 0.1
- Rationale: Wider valleys smooth the convolution, improving L2 norm
Mutation C (Add Peak in Wide Valley):
- Find the widest valley
- Create a new peak in the center with height = valley_height + 0.5
- Rationale: Multi-peak configurations beat single-peak step functions
Step 3: Probe and Evaluate
- Call probe_solution on ALL 3 variants (3 probes total)
- Rank by probe score
- Call evaluate_solution on TOP 1 only
Step 4: Iterate
- If beats record: continue with refined parameters
- If no improvement after 3 iterations: switch to Phase 2
## Phase 2: JAX Gradient-Based Optimization (iterations 13-22)
Step 1: Compute Gradients
- Use JAX autodiff: @jax.grad on the -c2_ratio objective
- Compute gradient w.r.t. each parameter
Step 2: Gradient-Ascent Step
- Take gradient step: new_param = param + 0.05 * gradient
- Clip parameters to valid range
Step 3: Variants from Gradients
Generate 2 variants:
- Variant 1: Follow positive gradient direction
- Variant 2: Follow negative gradient direction
Step 4: Probe and Evaluate
- Probe both, evaluate best
- If gradient norm < 0.001: switch to Phase 3
## Phase 3: Architecture Search (iterations 23-30)
Step 1: Try New Architectures
If stuck, keep best c2 but try architectural changes:
- Split Peak: Take one tall peak, split into two peaks with 0.7 * original height each
- Merge Valleys: Merge two adjacent valley intervals into one
- Three-Peak Asymmetric: Create three peaks with heights 1.2, 1.8, 1.0
Step 2: Final Evaluation
- Probe both variants
- Evaluate best
- Submit if c2 > 0.8962799441554086
## Key Rules
- ALWAYS call analyze_ratio_structure before mutation
- Use probes to filter: 5-6 probes before any full eval
- If iteration 12+ with no improvement: switch to Phase 2
