---
name: analytical-first
description: Always generate analytical candidates first, evaluate them, only then consider SGD-based hyperparameter tuning if no improvement.
---

# Analytical-First Strategy for Erdos C5

## Core Principle

The seed score (c5_bound ≈ 0.3809) comes from a pattern that SGD cannot improve.
Instead of training from random/sine seeds, USE ANALYTICALLY CONSTRUCTED step functions
that are GUARANTEED to have integral=1 and are structurally optimized.

## Workflow

### Phase 1: Analytical Screening (REQUIRED FIRST STEP)

1. CALL generate_analytical_candidates()
2. You will receive 8-9 candidates with precomputed c5_bound
3. Filter to c5_bound < 0.380 (typically 3-5 candidates)
4. CALL evaluate_solution on EACH filtered candidate
5. If ANY combined_score > 1.0 → CALL finish()

### Phase 2: Only if Phase 1 Fails

1. Call generate_analytical_candidates(temperature=0.8) for variety
2. Re-evaluate new candidates
3. Still stuck: Try ONE hyperparameter with num_restarts=1, num_steps=30000
4. Use probe_solution to screen before full eval

## Why Analytical Beats SGD

- Integral constraint is EXACT (SGD may violate it with penalty_strength)
- Golomb patterns are mathematically near-optimal for this problem
- No training overhead: c5_bound computed instantly
- Seed pattern quality ≈ analytical quality, SGD likely regresses

## Common Mistakes to Avoid

- ❌ Training SGD from scratch when analytical candidates exist
- ❌ Skipping analytical candidates to explore hyperparameters
- ❌ Using c5_bound >= 0.380 for full evaluation (wastes budget)
- ❌ Not checking ALL analytical candidates (pick the best 3-4)

## Expected Success

Golomb-4 or Golomb-5 patterns typically achieve c5_bound < 0.375,
which means combined_score > 1.02 (new record). One full eval should suffice.
