---
name: discovery-optimization
description: "Architecture-break exploration for C2 maximization. Generate diverse function families (Gaussian mixtures,\nB-splines, oscillatory decay, piecewise-linear, exponential/power-law bases), rank with probe_solution,\nevaluate top candidates, avoid refining step functions."
---

# C2 Breakthrough Protocol: Architecture Diversity Search

## Core Principle
The step-function record (0.89628) is a LOCAL optimum within the PIECEWISE-CONSTANT architecture.
To beat it, you MUST explore DIFFERENT mathematical ARCHITECTURES entirely.

## Phase 1: Generate Architectural Diversity (Every Iteration)

1. CALL generate_candidates at the start of EVERY iteration.
   - You MUST get proposals from DIFFERENT families each time.
   - If previous generation gave Gaussian mixtures, try B-splines this time.
   - If all were smooth, force at least one sharp/piecewise candidate.

2. Expected families to cover:
   - Gaussian mixtures: f(x) = Σ w_i * exp(-(x-μ_i)²/(2σ_i²))
   - B-spline basis: Optimize control points and knot positions
   - Oscillatory decay: f(x) = (1 + α*cos(βx)) * exp(-γ|x|)
   - Piecewise-linear: Linear segments with optimized breakpoints
   - Exponential/Power-law bases: Mixtures of exp(-λ|x|), |x|^α, etc.

## Phase 2: Probe-Based Filtering

1. For EACH candidate from generate_candidates, call probe_solution.
   - Use ALL 30 probes to rank all proposals.
   - Do NOT evaluate any candidate with probe score < current best (unless you have probes left and no better option).

2. Select top 2-3 candidates by probe score.

## Phase 3: Full Evaluation

1. Call evaluate_solution for each top candidate (1 eval each).
2. Track the best combined_score achieved.
3. If ANY evaluation beats current best, mark it as "promising family" and generate more from that family.
4. If no improvement after 3 evaluations, generate NEW candidates from a different architectural angle.

## Phase 4: Implementation

1. When editing with edit_solution, implement the FULL candidate architecture, not incremental changes.
   - Example: If candidate is a 3-Gaussian mixture, generate complete f(x) with optimized μ, σ, w.
   - Do not "adjust heights" of a step function. Start fresh.

## Phase 5: Recovery from Stalls

If stuck after 5 iterations with no improvement:
- Generate candidates from a COMPLETELY different angle.
- Example: If all were smooth functions, force piecewise-constant or oscillatory.
- Mix elements: Take structure from one family, parameters from another.

## Success Criteria
- combined_score > 1.039 (C2 > 0.89628)
- At least one proposal from a non-step-function family
