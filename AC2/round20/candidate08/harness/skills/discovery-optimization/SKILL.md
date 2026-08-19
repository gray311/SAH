---
name: discovery-optimization
description: "Systematic step-function tuning. The seed's 12 step-patterns already exceed the record.\nTune heights (\u00b10.1), widths (\u00b10.02), asymmetry (\u00b10.03) before trying new families.\nAlways probe before full eval."
---

# C2 Step-Function Tuning Protocol

## Core Principle
The seed's 12 step-patterns achieve C2 ≈ 0.8963 (score 1.042). These are CLOSE to optimal.
Small parameter adjustments (±5% height, ±2% width) can improve them. Do NOT jump to
Gaussian mixtures unless ALL 12 patterns are exhausted.

## Step Pattern Analysis
The seed implements _create_step_initializer with 12 patterns:
- Pattern 0: Single high step (height 1.40, 0.25-0.75)
- Pattern 1: Higher peak (1.50, 0.27-0.73)
- Pattern 2: Narrow high peak (1.60, 0.30-0.70)
- Pattern 3: 3-level asymmetric (0.90, 1.90, 0.90)
- Pattern 4: 3-level (1.10, 2.30, 1.40)
- Pattern 5: Two high steps (1.50 each)
- Pattern 6: 4-level (0.70, 1.30, 1.70, 1.00)
- Pattern 7: 5-level narrow peak (0.60-2.20-1.20-0.60)
- Pattern 8: Staircase (0.60, 1.00, 1.50, 1.20)
- Pattern 9: 5-level asymmetric (0.80-2.00-1.40-0.90)
- Pattern 10: Wide base + narrow peak (1.20-2.80)
- Pattern 11: Three peaks (1.50-2.50-1.50 and 2.50)

## Mutation Strategy (per pattern)
For each pattern, try these 3 mutations IN ORDER:

Mutation A (Height Boost): Increase peak height by 0.1
- Example: Pattern 1 (height 1.50) → 1.60
- Effect: Increases ||f★f||_∞, may hurt C2 if too high

Mutation B (Width Expansion): Expand interval by 0.02
- Example: Pattern 0 (0.25-0.75) → 0.23-0.77
- Effect: Widens support, may improve L2/inf ratio

Mutation C (Asymmetry Shift): Shift peak 0.03 left or right
- Example: Pattern 0 (0.25-0.75) → try 0.23-0.77 or 0.27-0.73
- Effect: Tests if symmetry is optimal

## Execution Flow
1. Start with Pattern 0, try Mutation A (probe), Mutation B (probe), Mutation C (probe)
2. Evaluate the best probed variant if probe score > 1.0
3. Move to Pattern 1, repeat
4. Continue through all 12 patterns
5. If after Pattern 11: still seed best, then try Gaussian mixture
6. Gaussian mixture: f(x) = w1*exp(-((x+1)²)/(2*σ²)) + w2*exp(-((x)²)/(2*σ²)) + w3*exp(-((x-1)²)/(2*σ²))
   with w=[0.33, 0.34, 0.33], σ∈[0.5, 0.8]

## Tool Usage
- edit_solution: Use f = f.at[start:end].set(new_value) for step patterns
- probe_solution: Call on ALL 3 mutations before any full eval
- evaluate_solution: Call ONLY on best mutation if all 3 probes > 1.0
- finish: Report which pattern had best improvement and what mutation helped

## Key Rule
EXHAUST the 12 seed patterns first. They are proven; new families are speculative.
Small changes to proven structures beat radical reinvention.
