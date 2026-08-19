---
name: parallel-family-exploration
description: Parallel exploration of orthogonal function families with structural analysis and probe-based filtering.
---

# C₂ Maximizer: Parallel Family Exploration

## Core Principle
Beat the step-function record by exploring MULTIPLE ORTHOGONAL FUNCTION FAMILIES IN PARALLEL from iteration 1, then deep-refine only winners.

## Phase 1: Parallel Exploration (iterations 1-40)

### Step 1: Generate Diverse Families
Call generate_candidates to get 5-7 proposals across DIFFERENT families:
- Gaussian mixtures: smooth multi-peaked functions
- B-spline basis: flexible smooth transitions
- Piecewise-linear: controlled smoothness
- Oscillatory decay: (1+α*cos(βx))*exp(-γ|x|)
- Multi-level asymmetric steps: refined step patterns
- Asymmetric exponential: different decay rates

### Step 2: Structural Analysis
For EACH new proposal, call analyze_convolution:
- Estimates peak count, symmetry, decay characteristics
- Provides recommendations: add peaks, widen function, adjust oscillation frequency
- Use insights to guide mutation strategy

### Step 3: Probe-Based Filtering
1. Call probe_solution on ALL proposals (30 probes total)
2. Rank by approximate combined_score
3. Select TOP 3-4 for full evaluation
4. Discard others, generate NEW proposals from different angles

### Step 4: Full Evaluation & Mixed Refinement
- Evaluate only promising proposals (probe score > current best or top 3)
- For winners: refine with targeted mutations
- But ALSO generate new proposals from OTHER families each iteration
- Don't let any family dominate >40% of evaluations

## Phase 2: Deep Refinement (iterations 41-60)
Only for families that beat the record:
1. AGGRESSIVE structural mutations: add/remove peaks, switch families, alter decay/frequency
2. Call analyze_convolution to guide: understand why current architecture is suboptimal
3. If stuck 5 iterations, switch to new family type

## Key Rules
- PARALLEL: Generate different families each iteration.
- STRUCTURAL: Call analyze_convolution to estimate convolution properties.
- PROBE FIRST: Always probe before full eval.
- DIVERSITY > DEPTH: No family dominates >40% of evals.
- MIX SUCCESS: Combine elements from winners to create new architectures.
