---
name: discovery-optimization
description: "Diverse initialization search for Erdos C5 minimization. Focus on exploring the 15 seed patterns\nwith different random seeds rather than hyperparameter sweeps. Use generate_ready_candidates for pre-scorings.\nIncrease penalty_strength if integral constraint violated. Increase num_intervals for finer search."
---

# Diverse Initialization Search for Erdos Problem

## Core Strategy

The seed program has 15 pattern-based initializations (patterns 0-14). The current harness wastes budget testing single hyperparameter changes.

## Correct Approach:

### Step 1: Leverage Existing Pattern Diversity

The seed's `_get_best_initialization` method tries 15 patterns (Golomb ruler, bipartite, tri-modal, random, etc.).

DO THIS INSTEAD: Modify seed to use ALL 15 patterns across different seeds:
For seed in [0, 1, 2, 3, 4]:
    For pattern in [12, 14, 5, 0, 8, 9]:  # Golomb, tri-modal, bipartite, random variants
        latent = _get_best_initialization(seed + pattern)
        h = jax.nn.sigmoid(latent)
        Check integral, train, evaluate

This gives 6 * 5 = 30 diverse initializations per evaluation.

### Step 2: Tool-Based Candidate Generation

**Use generate_ready_candidates:** This tool generates 3 pre-scorings (Golomb, Bipartite, Tri-modal) with computed c5_bound.
- If c5_bound < 0.375, call evaluate_solution
- If c5_bound >= 0.375, discard (waste of budget)

### Step 3: Escalation Strategy

If diverse initialization fails (all c5_bound > 0.385):

1. Increase penalty_strength to 120 - Current seed uses 60, which may not enforce integral=1 tightly
2. Increase num_intervals to 1600 - Finer grid captures more structure
3. Use num_steps=100000 - Longer training from better initializations

## Workflow

1. Call generate_ready_candidates once
2. Evaluate candidates with c5_bound < 0.375
3. If no improvement, edit seed to use patterns 12, 14, 5, 0, 8 with seeds 0,1,2,3,4
4. Use num_restarts=3, num_steps=100000, penalty_strength=120
5. If still no progress, increase num_intervals to 1600

## Why This Works

- Explores 15+ diverse initializations (vs seed's single best)
- Uses pre-scorings to avoid wasting evals on bad candidates
- Enforces integral constraint more strictly if needed
- Searches finer grid if structure is missed
