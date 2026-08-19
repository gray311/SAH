---
name: template-focused-search
description: Focus on generating diverse template structures first, then optimize. Don't over-tune hyperparameters.
---

# Template-Focused Search for Erdos C5

## Golden Rule: Structure > Hyperparameters

The best improvements come from BETTER TEMPLATE SHAPES, not better hyperparameters.

## Step 1: Generate Templates

Call generate_step_templates to get 8 different h(x) structures:
- bipartite_single: one threshold
- boundary_peak: peak near edge
- dual_peaks: two separated peaks
- tri_modal: three peaks
- symmetric_double: one wide peak centered
- asymmetric_taper: narrow peak + wide plateau
- golomb_ruler: four equally spaced peaks
- boundary_double: peaks at both edges

## Step 2: Pick 3 Templates to Test

Start with:
1. bipartite_middle (simplest, most stable)
2. boundary_peak (explores edge effects)
3. golomb_ruler (maximizes separation)

## Step 3: Optimize Each Template

For EACH selected template:
- Keep template structure fixed
- Vary ONE hyperparameter: num_steps, penalty_strength, or num_intervals
- Run full optimization with jax (not just edit the template)

## Step 4: Evaluate Best 2

After optimizing 3 templates:
- Pick the 2 with lowest c5_bound
- Run full evaluate_solution on each
- If either gives combined_score > 1.0, finish!

## Step 5: If No Improvement

Modify the BEST template structure slightly:
- Narrower peaks
- Different peak positions
- Add/subtract a small peak
- Regenerate and repeat

## Why Random Failed

Random h(x) values:
- Don't satisfy integral=1
- Have many small wiggles (high frequency)
- Optimize into bad local minima

Structured templates:
- Satisfy constraints by design
- Have controlled frequency
- Can be optimized in a consistent direction
