---
name: coarse-step-search
description: Search coarse step functions (3-7 jumps) with probe screening, then full evaluate. Focus on structured patterns, not continuous optimization.
---

# Coarse Step Function Search for Erdos Minimum Overlap

## Strategy

The seed optimizer searches continuous functions. But better solutions likely come from COARSE step functions with few jumps (3-7 intervals).

## Workflow

1. Use step_func_gen to get 8+ explicit step function definitions
2. For each, EDIT the seed to define h as a step function directly (no sigmoid)
3. Call probe_solution to quickly estimate C5 (500 intervals)
4. Keep candidates with probe C5 < 0.375 and integral approx 1
5. Call evaluate_solution on top 2-3 candidates
6. If no improvement, try BINARY step functions (h in {0,1}) with different supports

## Key Insight

The seed's 12 initialization patterns are all similar sigmoid shapes. They need COMPLETLY different structures. Step functions with few jumps are fundamentally different.

## Expected C5 Values

- Binary h=1 on [0,0.5]: C5 = 0.5
- Uniform h=0.5: C5 = 0.5
- Optimized step function: C5 < 0.38 (target)

Focus on finding step functions that distribute overlap evenly across all shifts k.
