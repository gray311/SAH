---
name: valid-h-screening
description: Generate valid h functions, edit seed to use ONE pattern with num_restarts=1, probe screen for c5_bound < 0.375, then evaluate top candidates.
---

# Valid H Screening for Erdos Optimizer

## Problem
The seed optimizer needs h: [0,2]->[0,1] with integral(h)=1.
Current harness generates invalid patterns. We need VALID h arrays.

## Strategy

### Phase 1: Generate Valid H Functions
Call generate_valid_h to get 4 valid h arrays (already in [0,1], integral=1).

### Phase 2: Edit Seed for Single Pattern
For each h pattern:
  1. EDIT _get_best_initialization to return a latent that, when sigmoided,
     gives approximately the target h pattern.
  2. Set num_restarts=1, seed_start=0
  3. Call probe_solution to check c5_bound estimate

### Phase 3: Evaluate Promising Candidates
Call evaluate_solution on candidates with c5_bound < 0.375.

### Phase 4: Iterate
If no improvement, generate a new h pattern and repeat.

## Why This Works
- generate_valid_h creates h in [0,1] with integral=1 exactly
- num_restarts=1 isolates ONE pattern's evaluation
- Probes screen quickly (10s each, separate budget)
