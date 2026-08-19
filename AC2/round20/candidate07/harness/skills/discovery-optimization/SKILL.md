---
name: discovery-optimization
description: "Systematic step-function parameter exploration. Within the working step-function\nframework, explore parameter space (boundaries, heights, asymmetry) using probes to\nrank variants before full evaluation. Reset to different patterns when stuck."
---

# C2 Maximizer: Systematic Step-Function Parameter Exploration

## Core Principle
Rather than attempting to generate new function families (which requires complex
code that easily breaks), focus on systematic parameter space exploration within
the step-function framework. The current best is a step function - perturb its
parameters and use probes to guide the search.

## Phase 1: Parameter Space Exploration (iterations 1-20)

Step 1: Analyze Current Structure
- Call analyze_step_structure on your best function
- Extract: step boundaries, heights, number of intervals
- Compute statistics: mean height, max height, boundary spacing

Step 2: Generate Controlled Variants
- Call generate_step_variants with 3-5 variants:
  * Variant A: Shift all boundaries by +2% of their position
  * Variant B: Shift all boundaries by -2% of their position
  * Variant C: Increase middle heights by +0.1, decrease by -0.1 elsewhere
  * Variant D: Increase number of intervals by +10% (if feasible)
  * Variant E: Create asymmetric variant (mirror current and adjust heights)

Step 3: Probe-Based Filtering
- Call probe_solution on ALL variants (3-5 probes total)
- Rank by probe score
- Call evaluate_solution on TOP 2 by probe score
- If probe score < 1.0: skip full eval

Step 4: Learn and Iterate
- Track which parameter changes led to improvement
- If both full evals fail: try different starting pattern (different pattern_idx)
- Continue until iteration 20 or improvement

## Phase 2: Gradient-Ascent Refinement (iterations 21-30)

1. Take best variant from Phase 1
2. Generate 3 variants with SMALL changes:
   - Boundary shifts of ±1%
   - Height adjustments of ±0.05
   - Try reversing asymmetry
3. Probe all, evaluate top 1
4. If no improvement after 5 iterations: go back to Phase 1 with new pattern

## Key Rules
- PARAMETER PERTURBATION > ARCHITECTURAL JUMPS
- Use 30 probes to explore 10-15+ parameter configurations
- If iteration 10-15 without improvement: reset to seed with different pattern
- Always analyze step structure to guide perturbations
