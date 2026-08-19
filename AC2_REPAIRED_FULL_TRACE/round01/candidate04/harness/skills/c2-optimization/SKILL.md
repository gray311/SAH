---
name: c2-optimization
description: Specialized playbook for maximizing the second autocorrelation inequality constant C₂ through step-function and piecewise-linear function design.
---

# C₂ Optimization Skill

## Objective
Maximize C₂ = ||f ★ f||₂² / ((∫f)² ||f ★ f||_{∞}) where f is a non-negative function.
Current record: 0.8962799441554086 (step functions)
Target: Exceed 0.8962799441554086

## Key Insights

### 1. Step Functions Dominate
The current champion uses step functions. Your optimization should:
- Start with a coarse piecewise-constant approximation
- Use sharp transitions (nearly discontinuous)
- Allow different step heights and widths

### 2. Piecewise-Linear Refinement
Instead of smooth transitions, use:
- Linear segments between key points
- Focus on optimizing the "corners" of the function
- Keep the function non-negative via softplus or max(0, x)

### 3. Symmetry Exploitation
- Even functions (f(-x) = f(x)) reduce complexity
- Consider symmetric step patterns around x=0

### 4. Strategic Discretization
- Use MORE intervals (100-200+) for sharper steps
- Coarse grid for exploration, fine grid for refinement
- Adaptive refinement around step boundaries

## Implementation Strategy

### Phase 1: Step Function Foundation
```python
# Initialize with step-like structure
# Use many intervals to approximate sharp transitions
# Start with a simple multi-step pattern
```

### Phase 2: Gradient-Based Refinement
- Use Adam or a more aggressive optimizer
- Warmup is important for stable convergence
- Consider learning rate scheduling (cosine decay)

### Phase 3: Structure Discovery
- Allow the optimizer to discover step locations
- Use multiple starting points for different step configurations
- Explore combinations of 3-7 steps initially

## Critical Parameters to Tune

1. **num_intervals**: Increase from 50 to 100-200 for sharper steps
2. **learning_rate**: May need higher initial LR (0.05-0.1)
3. **num_steps**: 15000 is reasonable, but consider 20000-30000
4. **warmup_steps**: 1000 is good for stability

## Common Pitfalls

- Smooth functions (Gaussian, exponential) underperform
- Too few intervals blur step boundaries
- Learning rate too low prevents escape from local minima
- Not enforcing non-negativity properly

## Evaluation Strategy

1. First evaluation: Test with 100 intervals, LR=0.05
2. If score < 0.9998, increase intervals to 200
3. If score < 0.9999, try LR=0.1 with warmup
4. Target: combined_score > 1.0 (C₂ > 0.8962799441554086)

## When to Restart

- If stuck at combined_score < 0.9997 after 2 iterations
- If gradient norm is consistently very small (< 1e-6)
- If loss plateauing after 10000 steps
