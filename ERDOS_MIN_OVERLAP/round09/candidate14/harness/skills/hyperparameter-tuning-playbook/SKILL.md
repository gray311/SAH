---
name: hyperparameter-tuning-playbook
description: Systematic approach to tuning optimizer hyperparameters for the Erdős problem. Use probe_solution to cheaply filter configs before full evaluation.
---

# Hyperparameter Tuning for Erdős C5 Problem

## Understanding the Hyperparameters

### Learning Rate (base_learning_rate)
- Too low (<0.001): Slow convergence, may not escape local minima
- Too high (>0.02): Unstable training, oscillations
- Good range: 0.005-0.015 for this problem

### Penalty Strength
- Constrains integral(h) to be exactly 1
- Too low (<500): Constraint violations, invalid solutions
- Too high (>10000): Over-penalization, optimizer struggles
- Good range: 2000-8000

### Number of Steps
- Too few (<20000): Inadequate training, stuck in local minima
- Too many (>80000): Diminishing returns, wastes budget
- Good range: 40000-60000

### Restarts (num_restarts)
- Helps escape local minima by trying multiple initializations
- Each restart costs full evaluation budget
- Good range: 2-4 (balance diversity vs budget)

### Discretization (num_intervals)
- More intervals = finer function representation
- Too few (<400): Loss of function detail
- Too many (>1200): Computationally expensive
- Good range: 600-900

## Tuning Strategy

1. Start with BROAD sweep: test 3-5 configs spanning the ranges above
2. Use probe_solution for each config (1000 steps each, cheap)
3. Keep configs with probe c5_bound < 0.38
4. Run full evaluation on top 2-3
5. If successful, NARROW the sweep around winning config
6. Repeat until budget exhausted or no improvement possible

## Common Pitfalls

- Don't change ALL hyperparameters at once - isolate what works
- Always check the probe_score before spending full evals
- Remember: you need c5_bound < 0.380923, so combined_score > 1.0
- Save intermediate best programs between iterations
