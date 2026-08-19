---
name: discovery-optimization
description: "Direct construction harness for C\u2085 bound optimization.\nUses constructive methods (step functions with enforced constraints) rather than gradient descent.\nTargets combined_score > 1.0 by finding c5_bound < 0.38092303510845016."
---

# C₅ Bound Optimization via Direct Construction

## The Problem

Minimize: max_k ∫₀² h(x)(1-h(x+k))dx
subject to: h:[0,2]→[0,1], ∫h=1

## Why Gradient Descent Fails

The seed's Adam optimizer with 12 initialization patterns is stuck because:
- High-dimensional latent space has many local optima
- Penalty-based constraint handling is weak (penalty_strength=1370 is not enough)
- 800 intervals is too fine for global optimization

## Direct Construction Strategy

### Step 1: Generate Candidates

Use `search_discrete_configurations` to automatically create 20-50 valid step functions.
This tool enforces all constraints and tries multiple patterns:
- Single-interval concentration
- Double-interval splits
- Uniform distributions
- Multi-step functions

### Step 2: Score with probe

Use `evaluate_c5_bound` to compute the C5 bound for each candidate.
This is FAST (uses FFT) and does NOT consume your evaluation budget.

### Step 3: Select and Submit

Pick the 3-5 best candidates (lowest c5_bound) and use `edit_solution` 
to replace the EVOLVE-BLOCK with code that returns these candidates directly.

Example edit strategy:
```python
def _get_initialization(self, seed):
    # Return pre-validated step function
    return jnp.array([0.5, 0.5, 0.0, ...])  # valid h with ∫h=1
```

### Step 4: Refine if needed

Once you find a promising candidate with c5_bound ≈ 0.37, try:
- More intervals (500-1000) for finer resolution
- Slightly different patterns
- But keep the direct construction approach

## Success Criteria

- combined_score > 1.0 means c5_bound < 0.38092303510845016
- With direct construction, you can test 50+ candidates in one evaluation
- Focus on simple patterns first: [1,0,...], [0.5,0.5,0,...], etc.

## Common Patterns to Try

1. Single step: h=1 on [0,0.5], h=0 elsewhere (integral=0.5×2=1) ✓
2. Two steps: h=0.5 on [0,1], h=0 elsewhere (integral=0.5×2=1) ✓
3. Triangle: linear from 0→1 at x=0.5, 1→0 at x=1.5
4. Uniform: h=0.5 everywhere (integral=0.5×2=1)

Remember: h must be in [0,1] and integrate to exactly 1 over [0,2].
