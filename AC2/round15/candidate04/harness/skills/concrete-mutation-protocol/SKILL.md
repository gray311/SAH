---
name: concrete-mutation-protocol
description: Execute templates as SEARCH/REPLACE edits to transform the seed code into new architectures.
---

# Concrete Mutation Protocol for C₂ Maximization

## Core Principle

Don't just talk about exploration. ACTUALLY EXECUTE mutations by replacing the seed's EVOLVE-BLOCK
with complete, syntactically valid Python code for a new function architecture.

## Phase 1: Template Selection (Each Iteration)

1. Call get_mutation_template to get ONE template for a DIFFERENT function family than you've tried.

2. Try these families:
   - Gaussian mixtures: f(x) = sum w_i * exp(-((x-mu_i)^2)/(2*sigma_i^2))
   - Piecewise-linear: Linear segments connecting optimized vertices
   - Oscillatory with decay: f(x) = (1 + alpha*cos(beta*x)) * exp(-gamma*|x|)
   - Asymmetric multi-level steps: Multiple levels with broken symmetry

## Phase 2: Concrete Execution

1. Generate a SEARCH/REPLACE edit that:
   - Finds "# EVOLVE-BLOCK-START" in the seed
   - Replaces everything to "# EVOLVE-BLOCK-END" with your new implementation
   - Ensures result is VALID Python defining C2Optimizer._objective_fn

2. Call edit_solution with the COMPLETE replacement code. Do NOT make small tweaks —
   REPLACE the entire function architecture.

## Phase 3: Evaluation

1. Call evaluate_solution ONCE to test your mutation.

2. If combined_score > 1.03896: You've beaten the record!

3. If combined_score ≤ 1.03896: Generate a NEW template (different family) and try again.

## Critical Rules

- NEVER refine one function type for 5+ iterations without trying a new architecture
- NEVER use probe_solution — evaluator is numerically sensitive
- ALWAYS call get_mutation_template before editing
- The edit must be complete, valid Python — ensure it works before submitting
