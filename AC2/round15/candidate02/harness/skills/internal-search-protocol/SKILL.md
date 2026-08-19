---
name: internal-search-protocol
description: Use local_search_optimizer to thoroughly explore neighborhoods before full evaluation.
---

# Internal Search Protocol for C₂ Maximization

## Core Principle

The step-function record (1.03896) is a LOCAL optimum. Small random perturbations fail.
Use local_search_optimizer to perform BOUNDED INTERNAL SEARCH - generate multiple variants,
probe them cheaply, and return the best. This is more effective than single-shot exploration.

## Protocol Steps

### Step 1: Initialize Internal Search (Iteration 1)

1. Call local_search_optimizer with num_variants=10, perturbation_strength=0.1
2. This tool will:
   - Generate 10 variants of the seed by perturbing pattern parameters
   - Probe all 10 variants (using 10 of your 30 probe budget)
   - Return the best variant with probe score
3. If probe score > 1.03896, call evaluate_solution ONCE to confirm
4. If confirmed improvement: proceed to Step 2. Otherwise, proceed to Step 3.

### Step 2: Diverse Proposal Refinement

For each diverse proposal (from generate_candidates):

1. Call local_search_optimizer with num_variants=5, perturbation_strength=0.15
2. This explores the neighborhood of the diverse proposal
3. If any internal variant has probe score > current best, evaluate it once
4. If improvement confirmed: refine with 1 more internal search

### Step 3: Stalled Recovery

If stuck after 10 iterations:

1. Call local_search_optimizer on current best with num_variants=15, perturbation_strength=0.25
2. This is a more aggressive search to escape the local optimum
3. If no improvement after 3 attempts: try completely new function families

## Key Rules

- ALWAYS use local_search_optimizer before calling evaluate_solution
- Probe budget is valuable: use it in internal search, not randomly
- Internal search is PARALLEL to diverse exploration, not a replacement
- NEVER refine the same variant >3 times without a new internal search
