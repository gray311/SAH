---
name: golomb-search-playbook
description: Use internal_golomb_search to systematically explore Golomb ruler parameterizations with mark count 3-8, kernel types, and widths. Then run phased optimization - exploration (lr=0.05, penalty=1000) -> refinement (lr=0.01, penalty=5000) -> fine-tuning (lr=0.001, penalty=20000).
---

# Golomb Search Playbook for Erdos Minimum Overlap

## Overview
The internal_golomb_search tool systematically explores Golomb ruler-based constructions with internal parameter optimization. This is critical because static patterns miss the optimal configuration.

## Step-by-Step Workflow

Step 1: Run Internal Search
Call internal_golomb_search() at the start of your edit. It will:
- Search over mark counts: 3, 4, 5, 6, 7, 8 marks
- Try both Gaussian and boxcar kernels
- Optimize mark positions via local search (15 steps of perturbation)
- Search over kernel widths (0.08, 0.12, 0.18)
- Use ctx.probe() for rapid evaluation during search
- Return the single best construction with parameters

Step 2: Extract Construction Parameters
From the returned construction, extract:
- mark positions (array of float)
- kernel type (gaussian/boxcar)
- kernel width(s)
- c5_bound from probe evaluation

Step 3: Phased Optimization
Use the construction as initialization for phased optimization:

Phase 1 (Exploration, 10000 steps):
- Learning rate: 0.05
- Penalty strength: 1000
- Goal: Escape local minima

Phase 2 (Refinement, 15000 steps):
- Learning rate: 0.01
- Penalty strength: 5000
- Goal: Fine-tune the solution

Phase 3 (Fine-tuning, 5000 steps):
- Learning rate: 0.001
- Penalty strength: 20000
- Goal: Enforce integral constraint and precision

Step 4: Evaluate Top Candidates
After optimization, use probe_solution to quickly check c5_bound.
Evaluate the top 2 candidates with evaluate_solution.

## Key Principles
- Search over parameters, not just fixed patterns
- Golomb rulers provide excellent starting points but need parameter tuning
- Use probe_solution during search, not evaluate_solution (budget efficiency)
- The best construction may have non-standard mark spacing or kernel width
