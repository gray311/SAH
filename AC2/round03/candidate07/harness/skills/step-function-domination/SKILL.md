---
name: step-function-domination
description: Method for conquering C2 through step function exploration. Step functions hold the current record (0.8963) and should be your PRIMARY focus, not the seed's piecewise-linear approach.
---

# Step Function Domination Protocol
## Mission

Beat the C2 record of 0.8963 by discovering superior step function configurations.

## Why Step Functions?

Historical evidence: Step functions achieved 0.8963. Smooth functions (Gaussian, exponential) typically score 0.88-0.89. The discontinuity in step functions may better concentrate the convolution energy.

## The Protocol

### Step 1: Generate Variants

Call generate_step_variants immediately. This returns 10 pre-structured step function templates covering:
- Width variations (narrow to wide)
- Height variations (tall to short)  
- Multi-level configurations (2-3 levels)
- Asymmetric patterns
- Disjoint region combinations

### Step 2: Probe All Variants

For EACH variant returned:
1. Use edit_solution to replace the current function definition
2. Call probe_solution (cheap, ~10s)
3. Record probe score
4. Repeat for all 10 variants

### Step 3: Select Top Candidates

Pick the 3 highest probe-scoring variants.

### Step 4: Full Evaluation

For each top-3 candidate:
1. Run 2-3 times with different random seeds
2. Call evaluate_solution for each run
3. Keep the highest score

### Step 5: Escalate or Reset

- If any score > 0.8963: CONGRATULATIONS, submit
- If all ≤ 0.8965: Try multi-level steps with varied heights
- If still stuck: Try Gaussian mixtures as backup

## Critical Insights

1. STEP FUNCTIONS ≠ PIECEWISE-LINEAR: They are fundamentally different representations
2. DIVERSIFY WITHIN STEPS: Try 10+ configurations, not just 1-2
3. EXPLORE BEFORE TUNE: Vary structure first, parameters second
4. RECORD EVERYTHING: Track which variant beat what

## Failure Modes to Avoid

- Tuning the piecewise-linear hyperparameters (this is the trap!)
- Spending evals on step functions before probing enough
- Giving up on step functions when first few probe low (need structural diversity)

Success = C2 > 0.8963. Anything less means you're still stuck in the seed's local optimum.
