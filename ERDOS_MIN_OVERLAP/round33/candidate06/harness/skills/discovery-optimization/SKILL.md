---
name: discovery-optimization
description: "Systematically construct step functions from mathematical families (threshold, multi-threshold, symmetric patterns) and screen them with probe_solution before full evaluation."
---

# Direct Construction Strategy for Erdos C5

## Core Principle
Optimal solutions are simple step functions. Construct candidates directly from mathematical families instead of analyzing and perturbing the current solution.

## Step 1: Generate Candidates via construct_step_function

Call construct_step_function with one strategy:
- "threshold": Single step function with cutoff at position p
- "two_threshold": Two steps creating a plateau
- "symmetric": Symmetric step function around x=1.0
- "multi_peak": Multiple narrow peaks

Each call returns a COMPLETE program with the step function defined.

## Step 2: Parameter Search

For threshold functions: Try different cutoff positions p in [0.3, 1.7]
For multi-threshold: Try different step positions and heights

## Step 3: Screening

1. Generate 3-5 candidates with different strategies
2. Call probe_solution on each to check c5_bound
3. Keep candidates with c5_bound < 0.385
4. Call evaluate_solution on the best 1-2

## Step 4: Refinement

If no improvement after trying different strategies, refine parameters:
- Adjust threshold positions in small increments
- Try symmetric variants

## Rules
- ALWAYS use construct_step_function to generate complete programs
- NEVER try to analyze the current solution first
- Focus on direct construction from simple mathematical forms
- Use probe_solution to screen before full evaluation
