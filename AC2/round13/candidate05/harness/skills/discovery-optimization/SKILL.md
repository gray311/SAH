---
name: discovery-optimization
description: "Systematic step-function refinement for C\u2082 maximization. Focus on small, controlled mutations to heights, widths, and positions of piecewise-constant patterns. Exploit the known optimality of step functions rather than exploring inferior smooth alternatives."
---

# C₂ Maximizer: Systematic Step-Function Refinement Protocol

## Core Principle

Step functions are the PROVEN solution class for this problem. DO NOT abandon them.
The seed's 13 step patterns are starting points - refine them systematically.

## Mutation Strategy

### Type 1: Height Perturbation (PRIMARY)
- Adjust one level's height by ±0.02 to ±0.08
- Example: [1.40, 1.90, 0.90] → [1.35, 1.90, 0.90] or [1.40, 1.98, 0.90]
- Try both increasing AND decreasing
- Test ONE variant per iteration

### Type 2: Width Expansion/Contraction
- Adjust one interval boundary by ±2% to ±5%
- Example: interval at 0.25n → 0.26n or 0.24n
- Expanding the "core" region (where function is highest) often helps
- Contracting the "wings" can reduce ||f★f||_∞

### Type 3: Center of Mass Shift
- Shift all boundaries by the same offset (±1-2%)
- Example: [0.25n, 0.75n] → [0.24n, 0.74n] (shifts center left)
- Breaks symmetry, can improve ratio

### Type 4: Asymmetric Level Adjustment
- For multi-level patterns, break exact symmetry
- Example: [1.40, 1.90, 0.90] → [1.38, 1.92, 0.88]
- Slightly tilt the height distribution

### Type 5: Pattern Class Switch (LAST RESORT)
- Only after 8-10 failed mutations on current pattern
- If doing 3-level patterns → try 4-level or 5-level
- If doing symmetric patterns → try asymmetric
- If doing narrow peaks → try wide plat

## Execution Protocol

1. **Analyze current pattern**: What levels? What heights? What symmetries?
2. **Pick ONE mutation type** from the above
3. **Generate ONE variant** with small perturbation
4. **Evaluate** with evaluate_solution
5. **Track results**: Which mutation types work? Which directions help?
6. **If improving**: Continue refining in that direction
7. **If stuck for 3-4 iterations**: Try a different mutation type
8. **If stuck for 8-10 iterations total**: Switch to a different pattern class

## Key Rules

- ONE variant per evaluation - don't test multiple at once
- SMALL perturbations - large changes likely to worsen
- STEP FUNCTIONS ONLY - no Gaussians, splines, or smooth functions
- REPEAT SUCCESS: If a mutation type works, try more variants of it
- ABANDON FAILURE: If a mutation type fails 3-4 times, try a different one
