---
name: discovery-optimization
description: "Generate 10 diverse latent-space initializations that seed the 59000-step JAX optimizer.\nEach pattern is designed to produce a good starting point for gradient-based optimization.\nPatterns: Golomb, Bipartite, Triangular, Multi-peak, and variations of the seed's initialization.\nAFTER generating seeds, RUN THE OPTIMIZER (edit_solution + evaluate_solution) on each.\nThe optimizer's training loop is where improvement happens - don't bypass it with precomputed evaluations."
---

# Erdos C5 Optimization with Optimized Seeding

## Core Principle
The seed optimizer (59000-step JAX training) ALREADY finds near-optimal solutions.
Our job: improve its INITIALIZATIONS, then let the optimizer do its job.

## Phase 1: Generate Diverse Seeds
1. CALL generate_optimizer_seeds()
   - Gets 10 diverse latent-space initializations
   - Each is designed for the 59000-step JAX training loop
   - All satisfy integral=1, h in [0,1]

2. FOR EACH seed candidate:
   - CALL edit_solution to set the EVOLVE-BLOCK's initial latent to this seed
   - CALL evaluate_solution to run the 59000-step optimizer
   - Record the combined_score

3. PICK THE BEST result across all 10 seeds

## Phase 2: If All Seeds Fail (combined_score <= 0.99997)
Only then try hyperparameter variations:
- num_intervals: 400, 1600, 3200
- base_learning_rate: 0.001, 0.01
- penalty_strength: 30, 100

## Critical Rules
- ALWAYS run the optimizer's 59000-step training - this is where improvement happens
- Don't waste evals on precomputed patterns - let the optimizer refine them
- Generate seeds ONCE, then run optimizer on each
- If seed optimizer finds combined_score > 1.0, finish immediately
