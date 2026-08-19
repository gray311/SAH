---
name: aggressive-step-diversification
description: Method for creating diverse step function families. Focus on structural variety (num steps, widths, heights, symmetry), probe 5-7 variants, eval top 2. Maximum 4 evals total.
---

# Aggressive Step Function Diversification

## Problem Diagnosis
The seed uses 9 step-like initializations achieving 1.02872. The current harness FAILED because it mutated optimizer hyperparameters instead of CREATING NEW STEP FUNCTION STRUCTURES.

## Solution: Structural Step Diversification

### Step 1: Analyze Seed Structure
The seed's _create_step_initializer creates step functions with:
- 9 different patterns
- Step widths: 0.25n, 0.33n, 0.5n, etc.
- Heights: 1.0, 1.18, 1.2, 1.5, etc.

### Step 2: Create DIVERSE Variants
Don't reuse seed patterns. Create NEW configurations:

**Family A: Fewer Steps**
- 2-step: Single wide peak, width 0.4n-0.6n
- 3-step: Left-center-right, asymmetric

**Family B: More Steps**
- 4-step: Bimodal with narrow valley
- 5-step: Multi-cluster

**Family C: Extreme Heights**
- High central peak: h=2.0-2.5
- Low baseline + high center: h_baseline=0.5, h_center=2.0

**Family D: Asymmetric**
- Left-biased: 60% mass on negative side
- Right-skewed: exponential-like decay

### Step 3: Probe Before Eval
1. Generate 5-7 step configurations (STRUCTURALLY diverse)
2. Probe each (call probe_solution)
3. Rank by probe score
4. Evaluate ONLY TOP 2

### Step 4: If Still Stuck
- Try polynomial: f(x) = exp(-alpha*|x|^beta), alpha in [0.1, 1.0], beta in [1.5, 3.0]
- Try Gaussian mixture: sum of 2-3 Gaussians with varied sigmas

## Critical Rules
- MAX 4 full evaluations
- Always probe 5+ variants before eval
- STRUCTURAL diversity: don't just tweak heights, change step count, widths, symmetry
