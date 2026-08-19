---
name: constructive-search
description: Guide for constructive search in Erdős C₅ optimization. Use explicit pattern generation with few breakpoints instead of 800-parameter gradient descent. Start coarse (50 intervals), explore structural classes, then refine.
---

# Constructive Search for Erdős C₅ Bound

## Core Idea
The optimal step function for the Erdős minimum overlap problem is likely a **combinatorial arrangement** with few breakpoints, not a smooth function found by gradient descent on 800 parameters.

## Why Gradient Descent Fails
- Landscape has many local minima
- The ∫h=1 constraint creates a narrow feasible region
- 800 parameters is too many for effective gradient search
- Small steps can't escape poor local optima

## Winning Strategy: Coarse-Grained Construction

### Step 1: Start with Coarse Discretization
- Set num_intervals=50 (not 800!)
- Design piecewise constant functions with 5-15 breakpoints
- This reduces the search space to manageable combinatorial choices

### Step 2: Explore Structural Classes
Systematically try different structural patterns:

**1. Single Block**
- h(x) = 1 for x ∈ [0, 1], 0 elsewhere
- Baseline: c5_bound ≈ 0.380923

**2. Split Blocks**
- h on [0, a] and [2-a, 2] with equal height = a
- Vary a ∈ [0.2, 0.8]
- Symmetry may reduce maximum overlap

**3. Multi-Block**
- 3-5 blocks at different positions
- Place to minimize pairwise overlap
- Example: blocks on [0,0.2], [0.6,0.8], [1.2,1.4], [1.8,2.0]

**4. Wave Patterns**
- h(x) ≈ 0.5 + amplitude * sin(2π(x-1))
- Or sigmoid-based smooth transitions
- Helps explore the "middle ground" solutions

**5. Concentrated Peaks**
- Narrow high-value regions separated by zeros
- Can achieve low overlap if peaks are well-separated

### Step 3: Optimization Within Each Class
- **Don't use Adam** for parameter tuning
- Instead: use small perturbations, evaluate, keep improvements (hill climbing)
- Or: enumerate discrete choices (breakpoint positions, block heights)
- Or: use evolutionary algorithms (random initialization, crossover, mutation)

### Step 4: Refinement Path
Once you find a promising pattern with 50 intervals:
1. Refine to 200 intervals (keep the same structure, more points per block)
2. Further refine to 800 intervals for final answer
3. Only then compute the definitive score

### Step 5: Budget Discipline
- You have ~30 evaluations total
- Try 5-8 different structural classes, not 30 small tweaks
- If a class shows promise (combined_score improves), invest more evals
- If not, move to the next class quickly

## Implementation Guidance

### Rewriting the Optimizer
Replace the ErdosOptimizer class with something like:

- Explicit candidate generation + local search
- Evolutionary algorithm over breakpoint configurations
- Grid search over structural parameters

### Key Changes
1. **num_intervals**: Start at 50, not 800
2. **Initializations**: Use explicit patterns, not random latent vectors
3. **Optimization**: Use evolutionary/hill-climbing instead of Adam
4. **Restarts**: 10-20 different structural seeds, not 12 random ones

## Expected Outcome
By focusing on combinatorial construction rather than continuous optimization, you should be able to find solutions with c5_bound < 0.380923, achieving combined_score > 1.0.
