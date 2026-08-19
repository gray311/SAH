---
name: discovery-optimization
description: "Erd\u0151s C\u2085 bound optimizer. Focus on explicit piecewise-constant constructions with few breakpoints. Avoid gradient descent traps. Target combined_score > 1.0 via direct mathematical construction."
---

# C₅ Bound Optimization via Direct Construction

## Why Gradient Descent Fails

The seed program uses gradient descent from sigmoid-initialized latents. All 12 initialization patterns converge to the same local optimum (~0.999641). This is a **construction problem**, not an optimization problem.

## Winning Strategy: Explicit Piecewise-Constant Functions

The best solutions are simple step functions with 2-5 breakpoints. Construct them directly:

### Pattern Class A: Single Block
h(x) = 1 for x ∈ [0,1], h(x) = 0 elsewhere
- Integral = 1 ✓
- Very simple overlap structure

### Pattern Class B: Two Blocks
h(x) = a for x ∈ [0,x₁], h(x) = b for x ∈ [x₁,2]
- Constraint: a·x₁ + b·(2-x₁) = 1
- Try symmetric cases: x₁=1, a=b=0.5

### Pattern Class C: Alternating Blocks
h(x) alternates between 1 and 0 on intervals
- E.g., [0,0.5]:1, [0.5,1.5]:0, [1.5,2]:1
- Integral = 0.5+0.5 = 1 ✓

### Pattern Class D: Concentrated Mass
h(x) = k on [0,1/k], h(x) = 0 elsewhere
- Integral = k·(1/k) = 1 ✓
- As k increases, h becomes more concentrated

## Execution Plan

1. **Start with explicit constructions** (not gradient descent):
   - Test single block: h=1 on [0,1]
   - Test symmetric two-block: h=0.5 on [0,1]
   - Test alternating blocks with varying ratios

2. **Use pattern_prober** to check constraint satisfaction cheaply
3. **Refine winning patterns** by adding breakpoints
4. **Only use gradient descent** if explicit construction fails to beat seed

## Tool Usage

- **pattern_prober**: Test if your proposed piecewise function satisfies constraints before full evaluation
- **edit_solution**: Replace the entire optimizer with explicit construction code
- **evaluate_solution**: Full score only after construction is valid

## Constraints Checklist

- h(x) ∈ [0,1] for all x
- ∫₀² h(x)dx = 1 (exactly, not approximately)
- Use few breakpoints (2-5) for simplicity
