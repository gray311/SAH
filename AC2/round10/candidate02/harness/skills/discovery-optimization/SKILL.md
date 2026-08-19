---
name: discovery-optimization
description: "Explore diverse function classes (step variants, smooth transitions, mixtures) and refine promising candidates with probes before full evaluation."
---

# C₂ Optimization Strategy

## Phase 1: Global Exploration
1. Call explore_function_classes to generate 50-100 diverse function candidates across these classes:
   - Step functions: 3 variants of seed patterns with different heights (±20%), widths (±15%), positions (±5%)
   - Smooth functions: 10 sigmoid/gaussian-like functions with varying widths, centers, amplitudes
   - Mixtures: 15 weighted combinations of 2-3 base functions
   - Asymmetric: 10 patterns with peaks shifted to different positions
   - High-resolution: 5 functions with 800+ intervals for fine control

2. Save promising candidates to scratch space:
   - Keep those with probe scores within 5% of best probe

3. Test each saved candidate with probe_solution (5-10 candidates)

## Phase 2: Focused Refinement
1. Identify the top 2-3 candidates from probing
2. For each, generate 5 refined variants:
   - Narrow the peak width by 5-10%
   - Increase peak height by 0.05-0.1
   - Shift peak position by ±2%
   - Add a small secondary bump near the peak
   - Smooth edges with sigmoid transitions

3. Probe these refined variants, keeping the best

## Phase 3: Evaluation
1. Evaluate only the top 3 candidates from probing
2. If any beat current best by >2%, restart refinement from the winner
3. If no improvement after 3 evals, go back to Phase 1 with new diversity

## Key Principles
- **Diversity first**: The seed may be a local optimum; explore different families
- **Probe to rank**: Never waste full evals on bad candidates
- **Small refinements**: Once you find a direction, refine gradually
- **Change structure**: Don't just tune parameters - try different function forms
- **Budget discipline**: With 30 evals, you can afford ~3 full evaluations per good candidate
