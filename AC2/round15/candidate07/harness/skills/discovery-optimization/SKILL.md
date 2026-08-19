---
name: discovery-optimization
description: "Parallel architectural search across function families with probe-based filtering. Explore Gaussian mixtures, splines, oscillatory decay, and multi-level steps in parallel. Abandon failing families immediately."
---

# C₂ Optimizer: Parallel Architectural Search Protocol

## Core Principle

The step-function record is a LOCAL optimum. Break through by exploring DIFFERENT function architectures in PARALLEL with PROBE-BASED FILTERING.

## Phase 1: Diverse Generation (Iteration 0)

1. CALL generate_candidates IMMEDIATELY to get 5 proposals across families:
   - Gaussian mixtures (smooth, multi-peaked)
   - B-spline basis (flexible smooth transitions)  
   - Piecewise-linear (controlled smoothness)
   - Oscillatory with decay (structured convolutions)
   - Multi-level asymmetric steps (refined steps)

2. EXPECTATION: At least one family should beat the step-function record.

## Phase 2: Probe-Based Ranking

1. For each of the 5 proposals, call probe_solution to get approximate scores.

2. You have 30 probes - use ALL of them to rank proposals.

3. Select TOP 2-3 by probe score for full evaluation. SKIP families with low probe scores.

## Phase 3: Full Evaluation

1. For each top proposal, call evaluate_solution ONCE to confirm.

2. If a proposal beats the record (combined_score > 1.03896): 
   - Keep it as current best
   - Generate NEW candidates from a DIFFERENT angle (don't over-refine)
   - You have 27-28 evals remaining - use them to explore more families

3. If NO proposal beats the record:
   - Generate a NEW set of candidates (don't refine losers)
   - Try completely different families

## Phase 4: Rapid Family Switching

- Never spend >2 iterations on a single family without trying another.
- If probe+eval fails to improve, ABANDON that family immediately.
- Parallel exploration > sequential refinement.

## Phase 5: Stagnation Recovery

After 5 iterations with no improvement:
- Call generate_candidates again
- Try opposite "flavor" (smooth↔sharp, symmetric↔asymmetric)
- Mix elements from multiple successful proposals

## Key Rules

1. PROBE FIRST, then EVALUATE (30 probes available!)
2. PARALLEL exploration of 5+ families at iteration 0
3. ABANDON failing families immediately (don't refine losers)
4. ONE eval per promising proposal, then move on
5. The goal is to find ANY function class that beats step functions
