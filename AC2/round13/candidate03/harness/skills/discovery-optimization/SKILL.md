---
name: discovery-optimization
description: "Portfolio management protocol for C2 maximization. Track which function families\nhave been exhausted, use probe-based filtering, and diversify when local optima detected.\n\nCore principle: Diversity beats depth when you're stuck in a local optimum."
---

# C₂ Maximizer: Portfolio Diversification Protocol

## Core Principle

The step-function record is a LOCAL OPTIMUM. Sequential refinement of one pattern class
ALWAYS fails. You MUST explore DIFFERENT function architectures in PARALLEL.

## Phase 1: Initial Diversity Generation (Iteration 1-2)

1. Call generate_candidates to get 4-6 proposals across DIFFERENT families:
   - Gaussian mixtures (smooth, multi-peaked)
   - B-spline basis (flexible smooth transitions)
   - Piecewise-linear (controlled smoothness)
   - Oscillatory with decay (structured convolutions)
   - Multi-level asymmetric steps
   - Mixture of decaying exponentials

2. EXPECTATION: At least one family should beat 1.03841

## Phase 2: Probe-Based Portfolio Filtering

1. For EACH proposal from generate_candidates:
   - Call probe_solution to get approximate score
   - Record: family type, probe score
   - You have 30 probes - this is YOUR MAIN FILTER

2. Rank all proposals by probe score (highest first)

3. SELECT top 3-5 for full evaluation ONLY

4. SKIP any proposal with probe score < current best (1.03841)

## Phase 3: Full Evaluation & Tracking

1. For each selected proposal, call evaluate_solution ONCE

2. Track in your reasoning:
   - Pattern family type
   - Number of consecutive evaluations on this family
   - Best score achieved for this family
   - Whether it beat the record (1.03841)

3. If a proposal beats the record:
   - Record the improvement
   - You get a 2-eval "grace period" before needing to diversify
   - Optionally make tiny refinements (5-10% parameter changes)

## Phase 4: Stalled Detection & Mandatory Diversification

YOU ARE STUCK if ANY of these conditions:
- 3+ consecutive evaluations on SAME pattern family with no improvement
- 2+ evaluations on SAME family without beating the record
- You have exhausted 15 iterations with no new family tried
- The last 3 evaluated patterns all scored < 1.03841

When STUCK:
1. Call analyze_function_class to understand why current approach failed
2. Call generate_candidates with FOCUS on families you haven't tried
3. Use probe_solution to filter quickly
4. Diversify immediately - do not continue refining the failed family

## Phase 5: Cross-Family Hybridization (Advanced)

If multiple families show promise but none beat the record:
- Take structural elements from successful families
- Create hybrid functions (e.g., Gaussian mixture + step function core)
- Probe and evaluate hybrids
- This is your LAST RESORT before exhausting all families

## Key Rules (MEMORIZE)

1. PARALLEL EXPLORATION > SEQUENTIAL REFINEMENT
2. PROBE BEFORE EVALUATE (30 probes are your filter)
3. DIVERSIFY WHEN STUCK (not when "might be stuck")
4. ONE FULL EVALUATION PER VARIANT (do not waste evals)
5. TRACK FAMILY STATS (consecutive evals, best score per family)
