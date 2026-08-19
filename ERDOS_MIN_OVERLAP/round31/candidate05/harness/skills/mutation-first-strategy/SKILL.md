---
name: mutation-first-strategy
description: Generate concrete mutations using mutation_generator, screen with probe, evaluate best.
---

# Mutation-First Strategy for Erdos C5

## Step 1
CALL mutation_generator with mutation_type="bipartite" to create h(x)=1 if x<1 else 0.

## Step 2
CALL probe_solution to check c5_bound < 0.382.

## Step 3
If bipartite fails, CALL mutation_generator with mutation_type="multi_modal" and centers=[0.4,1.0,1.6].

## Step 4
CALL probe_solution on multi-modal candidate.

## Step 5
If both fail, try mutation_type="spread_peaks" with num_peaks=5.

## Step 6
CALL evaluate_solution on best probe candidate (c5_bound < 0.380).

## Key Rules
- Use mutation_generator for concrete, structurally different candidates
- Always screen with probe_solution before evaluate_solution
- Do NOT do random hyperparameter tuning
