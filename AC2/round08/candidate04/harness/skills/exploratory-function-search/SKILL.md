---
name: exploratory-function-search
description: Playbook for systematically exploring diverse function families beyond the seed's step functions.
---

# Exploratory Function Search Playbook

## Core Philosophy

The seed program already achieves combined_score=1.034 with sophisticated multi-level step functions.
To improve, you must explore function classes COMPLETELY ORTHOGONAL to steps.

## Step 1: Baseline Analysis

CALL analyze_function_type immediately to understand:
- What function class the seed uses (likely "step")
- What tier it operates at ("baseline")
- What the recommendation is for next exploration

## Step 2: Systematic Family Exploration

Don't refine steps - explore ENTIRELY DIFFERENT families:

**Priority Order**:
1. **Splines**: Smooth, differentiable functions with local control
   - Call generate_function_candidate with family="spline"
   - Start with 10-15 knots, test cubic B-splines
   - Vary knot density and heights

2. **Mixtures**: Combinations of basis functions
   - Call generate_function_candidate with family="mixture"
   - Try Gaussian, exponential, and rational mixtures
   - Test different number of components (3-7)

3. **Hybrids**: Combine approaches
   - Call generate_function_candidate with family="hybrid"
   - Mix step bases with spline refinements
   - Try step-function-like with smooth transitions

## Step 3: Rapid Probing Protocol

For EACH new function candidate:
1. EDIT with the generated function
2. CALL probe_solution IMMEDIATELY
3. MODIFY parameters and probe again (3-5 iterations)
4. Only if probe consistently shows improvement, EVALUATE

Target: 3-5 probes per new function class before evaluation.

## Step 4: Escalation to Evaluation

Evaluate ONLY when:
- Probing shows consistent improvement over baseline (probe > seed's probe equivalent)
- You've tried at least 2 different function families
- The function class is fundamentally different from seed

After evaluation:
- If combined_score > 1.0: Refine that function class (parameter optimization)
- If combined_score <= 1.0: Abandon, try different family

## Success Checklist

- [ ] Called analyze_function_type at start
- [ ] Explored at least 2 DIFFERENT function families
- [ ] Used 15+ probes before first evaluation
- [ ] Each evaluation preceded by successful probing
- [ ] Attempted spline, mixture, and hybrid approaches
