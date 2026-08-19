---
name: structural-search-playbook
description: Explore fundamentally different function structures for Erdos optimization. Use generate_structural_candidates to get diverse patterns, then evaluate each. Don't stay in one structural family - sample broadly!
---

# Structural Search Playbook

## Core Principle

The seed optimizer generates functions using the same structural template
(sigmoid(modulation + noise)). All 15 seed patterns are variations of this
single family. To beat the seed, we must explore DIFFERENT structural families.

## Pattern Families to Explore

1. **Piecewise-constant**: Functions that are constant over intervals
   - 3-block (low-high-low), 4-block, etc.
   - Key parameter: threshold positions

2. **Sinusoidal modulation**: Functions modulated by sine waves
   - Single frequency: h(x) = sigmoid(A*sin(pi*x) + B)
   - Multiple frequencies: h(x) = sigmoid(sum of sines)
   - Key parameters: frequencies, amplitudes, phases

3. **Polynomial-modulated**: Functions with polynomial shapes
   - Quadratic bump: h(x) = sigmoid(A*(x-c)^2 + B)
   - Higher-order polynomials

4. **Multi-peak (Gaussian sum)**: Sum of localized bumps
   - h(x) = sigmoid(sum_i exp(-(x-xi)^2/sigma^2))
   - Key parameters: number of peaks, centers, widths

5. **Ramp/linear**: Functions with linear regions
   - h(x) = sigmoid(A*x + B) for monotonic shapes
   - h(x) = sigmoid(A*abs(x-c) + B) for V-shapes

## Workflow

1. CALL generate_structural_candidates(patterns=[list of desired patterns])

2. EXAMINE the output:
   - Check each candidate's integral (should be ~1.0)
   - Note the precomputed c5_bound

3. FILTER: Keep only candidates with integral ≈ 1.0 and c5_bound < 0.375

4. EVALUATE: CALL evaluate_solution on each kept candidate

5. ANALYZE: Which structural pattern performed best?
   - Piecewise? Sinusoidal? Multi-peak?
   - What parameters worked well?

6. ITERATE: CALL edit_solution to modify the winning pattern:
   - Change the structural parameters
   - Vary threshold positions, frequencies, amplitudes
   - CALL evaluate_solution again

7. If no pattern beats seed, try a NEW structural family you haven't explored.

## Example Iterations

Iteration 1:
  - Generate 5 patterns (piecewise, sin1, sin2, quad, multi-peak)
  - Evaluate all 5
  - Best: piecewise-3 with c5_bound=0.378 -> combined_score=1.001

Iteration 2:
  - Edit piecewise pattern: change thresholds to [1/4, 1/2, 3/4]
  - Evaluate: c5_bound=0.382 (worse)

Iteration 3:
  - Try new family: ramp functions h(x) = sigmoid(A*x + B)
  - Evaluate best ramp: c5_bound=0.375 -> combined_score=1.018 (BEAT SEED!)
  - CALL finish
