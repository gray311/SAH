---
name: discovery-optimization
description: "Multi-phase diverse exploration for C\u2082 maximization. Use probe_solution to rank candidates from generate_candidates, then evaluate only top prospects. Systematically cycle through function families (gaussian, spline, piecewise, oscillatory, multi-step) rather than refining one type exhaustively."
---

# C₂ Maximizer: Diverse Family Exploration Protocol

## Phase 1: Establish Baseline
1. Evaluate the seed program ONCE to confirm baseline ≈ 1.03896
2. Record this as `current_best` for all future comparisons

## Phase 2: Probe-First Diverse Exploration
1. Call `generate_candidates` to get 3-5 proposals across DIFFERENT families:
   - gaussian_mixture: weighted sum of Gaussians
   - bspline: B-spline with optimized control points
   - piecewise_linear: linear segments
   - oscillatory_decay: cosine * exponential decay
   - multi_level_improved: refined multi-step with asymmetric heights

2. For EACH proposal:
   - Call `probe_solution` immediately (30-probe budget!)
   - Compare probe score to `current_best`
   - If probe < current_best: SKIP full evaluation, try next proposal
   - If probe >= current_best: schedule for full evaluation

3. After probing all candidates:
   - Call `evaluate_solution` only on TOP 3-5 by probe score
   - Track which family/class achieved improvement

## Phase 3: Limited Refinement
1. If a new family beats `current_best`:
   - Try 1-2 small refinements:
     * Height adjustment: ±0.05 on step heights
     * Width adjustment: ±5% on interval boundaries
     * Asymmetry: make heights slightly unequal
   - Probe before each refinement
   - Evaluate only if probe shows promise

2. If NO improvement after 2 refinement attempts:
   - STOP refining this family
   - Go back to Phase 2 with NEW candidates

## Phase 4: Escalation Strategy
If stuck after 15 iterations with no improvement:
1. Call `generate_candidates` with NEW angles:
   - Try completely different mathematical forms
   - Consider: is the optimum smooth or sharp? single-peaked or multi-peaked?
2. If stuck after 25 iterations:
   - Report best found, even if still below record
   - The step-function record may be very hard to beat

## Key Principles
- PROBE FIRST: Never evaluate without probing (you have 30 probes!)
- PARALLEL EXPLORATION: Cycle through families, don't exhaust one
- SKIP FAST: Probe < current_best means skip full eval
- LIMITED REFINEMENT: 1-2 tweaks max per successful family
- ESCALATE: When stuck, generate completely new candidates

## Tools Guide
- `generate_candidates`: Get diverse function proposals (call early!)
- `probe_solution`: Quick approximate score (use for EVERY candidate before full eval)
- `evaluate_solution`: Full score, budget-limited (call only on probe-passed candidates)
- `edit_solution`: Implement the chosen function
- `finish`: Report best C₂ and the function class that achieved it
