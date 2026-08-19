---
name: c2-discovery-strategy
description: A mathematical discovery playbook for optimizing C₂ constant. Call this when exploring novel function structures beyond the seed. Use c2_analyzer() for initial analysis, c2_probe() for rapid ranking, then evaluate_solution() to confirm.
---

# C₂ Discovery Playbook

## The Challenge
Maximize C₂ = ||f★f||₂² / (||f★f||₁ ||f★f||_∞)

The seed achieves 1.03431. To beat this: explore mathematical structures the seed hasn't tried.

## Phase 1: Initial Analysis
Call c2_analyzer() ONCE at the start. It returns:
- seed_structure_analysis: Why current seed works
- convexity_info: Which parameter spaces are convex
- recommended_function_classes: What to try
- exploration_directions: Specific modifications
- sensitivity_variants: 3 tested parameter changes with their C₂ scores

## Phase 2: The Probe-Then-Eval Loop
For each hypothesis:
1. EDIT: Implement your idea in edit_solution()
2. PROBE: Call c2_probe() - get fast ranking on 100-point grid
3. DECIDE: 
   - If coarse_grid_score < best_probe: REVERT, try different direction
   - If coarse_grid_score > best_probe + 0.02: CONFIRM with evaluate_solution()
   - If similar to best_probe: Try orthogonal modification
4. RECORD: Update your mental best probe score

## Phase 3: Systematic Exploration
Try each function class:

A. Piecewise Constant (Expand Seed)
   - Start with 6 levels: heights [0.5, 1.0, 1.8, 2.2, 1.0, 0.5]
   - Try asymmetric: peak at 0.3-0.7 range
   - Modify existing patterns by ±10%

B. Smooth Splines
   - Replace sharp steps with sigmoid transitions
   - Use cubic splines between step levels
   - Test 3-5 knot positions

C. Multi-Scale
   - f(x) = envelope(x) × piecewise(x)
   - Try Gaussian, exponential, polynomial envelopes

D. Fourier-Based
   - Work in frequency domain
   - Optimize Fourier coefficients with positivity constraints

## Phase 4: Budget Management
- You have 30 evaluations total
- Use probes to filter: only evaluate if c2_probe > 1.02
- Reserve 5-10 evals for final convergence

## Golden Rules
1. NEVER copy the seed exactly - you must FIND novel structures
2. ALWAYS call c2_probe() after edits before full evaluation
3. Track your best probe score mentally
4. Explore BEFORE optimizing - diversify first, then refine
