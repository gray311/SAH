---
name: discovery-optimization
description: "Architectural innovation for C\u2082 maximization. Generate diverse function families (multi-modal, ramp, oscillatory, B-spline) and use probe-based filtering to find architectures with flatter convolution peaks. Avoid incremental step-pattern refinement."
---

# C₂ Maximizer: Architectural Innovation Protocol

## Core Principle

Step functions are LOCAL optima with concentrated convolutions. Beat them by finding function
classes that produce FLATTER convolution peaks while maintaining L2 energy.

## Phase 1: Generate Diverse Architectures (Iteration 1)

1. Call generate_candidates to get 3-5 proposals across DIFFERENT architectures:
   - Multi-modal: Gaussians mix, piecewise bumps at asymmetric positions
   - Ramp functions: Triangular, trapezoidal shapes with smooth transitions
   - Oscillatory: (1+αcos(βx))·exp(-γ|x|) with optimized parameters
   - B-spline: Spline basis with optimized control points/knots

2. EXPECTATION: Each proposal should have fundamentally different spectral properties

## Phase 2: Probe-Based Ranking

1. For EACH proposal, call probe_solution (cheap, 10% subsample, separate 30-budget)
2. RANK all proposals by probe score
3. Select TOP 3-5 for full evaluation

## Phase 3: Full Evaluation & Quick Refinement

1. Call evaluate_solution ONCE per top proposal
2. If a proposal beats record (combined_score > 1.03896):
   - Try ONE tiny refinement (e.g., adjust one parameter by 5%)
   - Probe the refinement, evaluate if promising
   - BUT: After at most 2 refinements, generate a NEW architecture
3. If no proposal beats record: Generate a new set of candidates

## Phase 4: Stall Recovery

If 5+ iterations without improvement:
- Force switch: Pick an architecture you haven't tried (e.g., if only did smooth functions, try piecewise)
- Never refine the same architecture >3 iterations

## Key Rule

ARCHITECTURAL INNOVATION > PARAMETER TUNING. When one architecture plateaus, immediately explore a new family.

Why this works: Step functions have concentrated convolutions. Multi-modal, ramp, and oscillatory
functions naturally produce flatter convolution peaks - the key to beating C₂=0.89628.
