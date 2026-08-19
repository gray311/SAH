---
name: discovery-optimization
description: "C2 maximization via DIVERSE function family exploration. Test steps, splines, mixtures - don't lock into one class."
---

# C2 Maximization: Explore DIVERSE Function Families

## Core Principle

The seed already has sophisticated step function patterns. To improve, you must EXPLORE COMPLETELY DIFFERENT FUNCTION CLASSES, not just more complex steps.

## Function Families to Explore

1. **Step Functions** (baseline): Already in seed - use as starting point
2. **Spline Functions**: Smooth transitions, polynomial pieces - test B-splines, cubic splines
3. **Mixture Models**: Weighted combinations of Gaussians, exponentials, and simple functions
4. **Truncated Polynomials**: Polynomials with cutoff regions
5. **Fourier-based**: Functions designed in frequency domain

## Exploration Workflow

### Step 1: Analyze Current Best

CALL analyze_function_type on the seed to understand:
- What function type works best (likely multi-level steps)
- Score characteristics (c2 value, combined_score)
- What makes it successful

### Step 2: Generate Completely Different Classes

CALL generate_function_candidate with DIFFERENT family types:
- family: "spline" (test cubic B-splines with optimized knots)
- family: "mixture" (test Gaussian/exponential mixtures)
- family: "polynomial" (test truncated polynomial forms)

### Step 3: Rapid Probing

After editing for a NEW function class:
- CALL probe_solution IMMEDIATELY (don't evaluate)
- Repeat 3-5 times with different parameters
- Only if probe score suggests improvement, proceed to evaluate

### Step 4: Select and Evaluate

If a new function class shows promise in probing:
- CALL evaluate_solution ONCE to confirm
- If combined_score > 1.0, iterate to refine that class
- If not, abandon and try a different family

## Critical Success Factors

- **DON'T** keep refining step functions - the seed already optimized those well
- **DO** explore orthogonal function spaces (smooth vs discontinuous, local vs global support)
- **DO** use probes liberally (30 budget) to rank before evaluation
- **DO** change the fundamental mathematical form, not just parameters

## Checklist

- [ ] Analyzed what makes seed successful
- [ ] Generated a function from a DIFFERENT family than step
- [ ] Probed 3+ variants before evaluation
- [ ] Only evaluated if probe suggests genuine improvement
