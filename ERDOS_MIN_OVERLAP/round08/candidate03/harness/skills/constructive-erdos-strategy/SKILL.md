---
name: constructive-erdos-strategy
description: Construct mathematical step functions for Erdős overlap minimization. Use structured constructions before gradient refinement. Exploit symmetry, concentration, and multi-scale patterns.
---

# Constructive Strategy for Erdős C5 Bound Optimization

## Core Principle
Don't rely solely on gradient descent from random starts. **Construct** candidate step functions with mathematically-informed structures.

## Construction Patterns

### 1. Symmetric Constructions
- Functions symmetric around x=1 often achieve lower max overlap
- Try: h(x) = h(2-x) for symmetry
- Use sin/cos basis functions centered at x=1

### 2. Concentrated Mass Patterns
- Concentrate h(x) in regions where it doesn't self-overlap much
- Try: Gaussian-like concentration, then perturb
- Test different concentration centers (0.5, 1.0, 1.5)

### 3. Multi-Scale Patterns
- Combine coarse and fine scale structures
- Coarse: broad shape (sin/cos at low frequency)
- Fine: high-frequency modulations
- This escapes simple local optima

### 4. Boundary Focused
- Concentrate mass near x=0 and x=2
- Reduces overlap with shifted versions
- Use: h concentrated near boundaries, low in middle

## Refinement Strategy

1. **Construct** 3-5 diverse candidates using `construct_step_function`
2. **Evaluate** each to identify promising ones (combined_score > 0.99)
3. **Refine** promising candidates:
   - Increase num_intervals if discretization is coarse
   - Tune hyperparameters (learning_rate, penalty_strength)
   - Run multi-restart optimization from the constructed candidate
4. **Iterate**: If no improvement, construct with different pattern types

## Key Mathematical Insights

- The constraint ∫h=1 is critical: violated constraints destroy solutions
- Symmetric constructions often beat asymmetric random starts
- Multi-scale beats single-scale: captures both global structure and local detail
- Gradient refinement needs good starting points; construction provides those
