---
name: pattern-screening-workflow
description: Use generate_patterns to find novel initializations, train fast (30000 steps), probe to screen, evaluate top candidates.
---

# Pattern-First Search Workflow

## Core Principle

The seed optimizer's 15 patterns all converge to similar solutions. To find c5_bound < 0.380923, you MUST explore NEW pattern structures.

## Step 1: Generate Novel Patterns

CALL generate_patterns(seed=42, num_patterns=5) to get 5 diverse initializations:
- gaussian_2peaks: Bell curves at 0.5 and 1.5
- sparse_3spikes: 3 narrow high regions
- triangular: Single peak at center
- asymmetric_bimodal: High on [0,0.7], low on [1.3,2]
- quad_modal: 4 narrow peaks at 0.25, 0.5, 0.75, 1.0

## Step 2: Quick Analytical Filtering

Examine the returned c5_bound values:
- SKIP patterns with c5_bound >= 0.38 (not promising)
- KEEP patterns with c5_bound < 0.375 (worth training)

## Step 3: Fast Training & Probe

For each kept pattern:
1. EDIT to set that pattern's latent values
2. Set num_restarts=1, num_steps=30000
3. CALL probe_solution
4. If c5_bound < 0.372, proceed to full eval

## Step 4: Full Validation

CALL evaluate_solution on the best probed candidate.
If combined_score > 1.0, you have a new record!

## Budget Management

- 60 full evals budget
- Use probe to filter: only 2-3 full evals needed if you screen 5 patterns well
- Fast training (30000 steps) lets you train 5 patterns in one iteration

## Expected Outcome

With this workflow, you should find c5_bound < 0.375 within 3-5 evals,
potentially reaching combined_score > 1.0.
