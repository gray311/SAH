---
name: discovery-optimization
description: "Analytical screening for Erdos C5 minimization. Use generate_ready_candidates to create integral-constrained initializations, filter by precomputed c5_bound via FFT, then evaluate only the best. Avoid hyperparameter tuning - the bottleneck is initialization quality, not training hyperparameters."
---

# Analytical Screening Strategy for Erdos Problem

## Core Insight

The bottleneck is NOT training hyperparameters - it is the quality of initializations. The seed optimizer tries 15 random patterns, but we need STRUCTURED patterns based on the mathematics of the Erdos problem.

## Step 1: Generate Candidates (NO COST)

1. CALL generate_ready_candidates(temperature=0.5)
   - Returns 3 candidates, each with:
     * h: latent vector (already sigmoided)
     * integral: verified to be ~1.0
     * c5_bound: precomputed via FFT (exact, no training)
     * pattern_type: description of the pattern

2. EXAMINE the results:
   - Golomb patterns: marks at [0.0, 0.4, 0.8, 1.2, 1.6] - optimal spacing
   - Bipartite: threshold at some point a 
   - Tri-modal: 3 peaks at strategic locations

## Step 2: Filter by Precomputed Score

3. CHECK c5_bound for each candidate:
   - c5_bound < 0.370: EXCELLENT - call evaluate_solution IMMEDIATELY
   - c5_bound < 0.375: GOOD - call evaluate_solution
   - c5_bound < 0.380: MARGINAL - consider but low priority
   - c5_bound >= 0.380: SKIP - waste of eval budget

4. CALL evaluate_solution ONLY on candidates with c5_bound < 0.375
   - Full training (59000 steps) is expensive
   - We have 30 evals - waste them efficiently!

## Step 3: Escalate if Needed

5. If NO candidate with c5_bound < 0.375:
   - CALL generate_ready_candidates(temperature=0.8) - more diversity
   - EXAMINE results, filter again
   - If still no good candidate:
     * CALL generate_ready_candidates(temperature=1.0)
     * Or try num_restarts=10 with generate_ready_candidates(temperature=0.5)

6. If STILL stuck after 3 calls:
   - Accept that this task requires fundamentally new patterns
   - Consider calling generate_ready_candidates 4-5 times to exhaust the space

## Expected Outcome

With analytical screening, you should find c5_bound < 0.37 candidates within 1-2 tool calls.
Each good candidate costs 1 eval for confirmation. Budget: 30 evals means you can test 30+ candidates.

DO NOT spend time editing hyperparameters in the seed optimizer - the real lever is the INITIALIZATION.
Structured, mathematically-motivated patterns outperform random initialization by orders of magnitude.
