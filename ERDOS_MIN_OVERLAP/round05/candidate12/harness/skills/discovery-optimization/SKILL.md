---
name: discovery-optimization
description: "Mathematically-guided optimization of Fourier-based step function constructions. Use for harmonic analysis\nand overlap-minimization tasks where the seed is near-optimal. Focus on principled construction improvements\nand careful hyperparameter tuning rather than random exploration."
---

# Mathematical Optimization for Fourier-Based Step Functions

## Problem Understanding
You're optimizing a step function h: [0,2] → [0,1] to minimize max_k ∫ h(x)(1-h(x+k)) dx.
The seed achieves ~0.999641 (C5 ≈ 0.381), near the best known bound of 0.380923.

## Search Strategy
1. **INITIALIZATION ENHANCEMENTS**:
   - Try asymmetric two-level patterns: h(x) = a for x in [0, t], 1-a for x in [t, 2]
   - Calculate t to satisfy integral(h) = 1, then optimize 'a'
   - Try three-level patterns with specific transition points (e.g., 1/3, 2/3)
   - Increase the 12 patterns to 20-30 with more mathematical structure

2. **OPTIMIZER ADJUSTMENTS**:
   - The seed's lr=0.0053 may be too high; try 0.001-0.003 for more stability
   - Consider gradient clipping or AdamW instead of Adam
   - The seed uses 59000 steps; verify this is enough

3. **CONSTRAINT HANDLING**:
   - The penalty_strength=1370 forces integral(h)=1 but may prevent finding the optimum
   - Try a softer constraint or Lagrange multiplier approach

4. **TARGETED EDITS**:
   - When editing, focus on ONE change: add one pattern, adjust one hyperparameter
   - Always evaluate before moving on; learn from failures
   - If score drops, the direction was wrong; try a genuinely different idea

## Example Improvements
- Add asymmetric initialization: x = jnp.linspace(0, 2, N); a = 0.5; t = 2 * (1-a); h = jnp.where(x < t, a, 1-a)
- Try multi-restart with different initial 'a' values instead of random seeds
- Reduce penalty_strength if constraint is too restrictive

## Evaluation Feedback
- combined_score > 1 means C5 < 0.380923 (NEW RECORD)
- combined_score ≈ 1 means near-optimal
- combined_score < 1 means worse than seed

Be patient and methodical. This is a precision mathematical problem, not a brute-force search.
