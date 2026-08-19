---
name: architectural-exploration
description: Try fundamentally different solver designs, not parameter tweaks.
---

# Architectural Exploration for Erdos C5

## Core Principle
The seed solver (800 intervals, gradient descent) is stuck in a local minimum.
You need a DIFFERENT search strategy, not better parameters.

## Step 1: Choose a New Architecture

### Coarse-to-Fine
- Start with N=10 intervals, optimize simple step function
- Use hill climbing or simulated annealing
- Gradually increase to N=50, 100, 200

### Explicit Plateaus
- Define h as sum of N rectangular functions: h(x) = sum h_i * I(p_i <= x < p_i + w_i)
- Variables: positions p_i, widths w_i, heights h_i
- Constraint: sum(h_i * w_i) = 1
- Start with N=3-5, optimize, then add more plateaus

### Sparse Peaks
- h has 3-5 narrow peaks at strategic positions
- Example: peaks at 0.33, 1.0, 1.66
- Benefit: Clear separation, low self-overlap

### Symmetric Pattern
- h(x) = h(2-x), symmetric around x=1
- Define only half, mirror it
- Benefit: Regular structure, easier optimization

## Step 2: Implement and Evaluate
1. Write clean code for your chosen architecture
2. Call probe_solution (check c5_bound < 0.382)
3. If promising, call evaluate_solution
4. If combined_score > 1.0, finish!

## Key Rules
- NEVER just change hyperparameters of the seed solver
- ALWAYS try a fundamentally different approach
- SIMPLE is better than complex
- Keep constraints explicit (integral=1, h in [0,1])
