---
name: discovery-optimization
description: "Generate fundamentally different structural patterns for the Erdos function.\nPatterns must have qualitatively different shapes: piecewise, sinusoidal, multi-peak, etc.\nThis enables exploration of diverse regions of function space."
---

# Structural Diversity Strategy

## Problem
The seed optimizer generates functions using sigmoid(modulation + noise). All 15 seed patterns
are variations of this single family. We need to explore DIFFERENT function families.

## Solution: Structural Pattern Library

Generate candidates from these fundamentally different structures:

### Pattern 1: Piecewise-Constant (3 blocks)
h(x) = 0 for x in [0, 1/3], c for x in [1/3, 2/3], 0 for x in [2/3, 2]
Normalize so integral = 1. This creates a "centered blob" function.

### Pattern 2: Two-Block with Offset
h(x) = a for x in [0, a], b for x in [a, 2-a], a for x in [2-a, 2]
Adjust a and the levels so integral = 1. Creates asymmetric coverage.

### Pattern 3: Sinusoidal (1 frequency)
h(x) = sigmoid(A*sin(pi*x) + B) with A > 1 to create clear peaks/troughs.

### Pattern 4: Sinusoidal (2 frequencies)
h(x) = sigmoid(A*sin(2*pi*x) + B*sin(4*pi*x) + C) - creates more complex oscillations.

### Pattern 5: Quadratic Bump
h(x) = sigmoid(A*(x-1)^2 + B) - creates a single centered peak.

### Pattern 6: Multi-Gaussian
h(x) = sigmoid(sum_{i=1..k} exp(-(x-xi)^2/sigma^2)) for k=3,4 peaks.

## Workflow

1. CALL generate_structural_candidates(patterns=["piecewise3", "twoblock", "sin1freq", "sin2freq", "quadbump"])

2. EXAMINE all 5 candidates:
   - Verify integral ≈ 1.0
   - Note the c5_bound (precomputed)

3. CALL evaluate_solution on ALL candidates with integral ≈ 1.0 and c5_bound < 0.38

4. If any achieve combined_score > 1.0, CALL finish immediately.

5. If none beat seed, pick the BEST performer and CALL edit_solution to:
   - Vary the structural parameters (threshold positions, frequencies, amplitudes)
   - CALL evaluate_solution again

6. Repeat steps 1-5 until budget exhausted or score > 1.0.

## Why This Works

- Structural diversity: Each pattern family has different global shape properties
- The seed's 15 patterns are all "sigmoid + modulation + noise" - you need to break this mold
- Testing 5 diverse structures with 1 full eval each = 5 evals to find good directions
