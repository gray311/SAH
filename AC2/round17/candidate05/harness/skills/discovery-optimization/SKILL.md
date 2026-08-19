---
name: discovery-optimization
description: "Parallel architecture exploration: generate diverse function families from iteration 1, probe all to rank, evaluate top winners, exploit dominant family type."
---

# C₂ Maximizer: Parallel Architecture Exploration Protocol

## Core Principle
The seed step functions are already near-optimal (0.913). To beat them, explore DIFFERENT architectures in PARALLEL from iteration 1.

## Phase 1: Parallel Exploration (iterations 1-15)

### Step 1: Generate Diverse Candidates
Call generate_candidates immediately. Get 5 proposals across:
- Gaussian mixtures: weighted sum of Gaussians with optimized μ, σ, weights
- B-spline basis: 30-50 control points with softplus positivity
- Oscillatory decay: (1 + α cos(βx)) * exp(-γ|x|)
- Piecewise-linear: linear segments connecting optimized vertices
- Multi-level asymmetric steps: finer-grained than seed patterns

### Step 2: Probe-Based Ranking
For EACH proposal:
1. Call edit_solution to implement the concrete function
2. Call probe_solution to get approximate score
3. Record probe scores

You have 30 probes - use them to rank ALL 5+ proposals BEFORE any full evaluation.

### Step 3: Select and Evaluate Top Winners
- Select top 3 proposals by probe score
- Call evaluate_solution ONCE per proposal (max 3 full evals)
- If any beats record (combined_score > 1.0): mark as promising family
- If none beat record: call generate_candidates again with different families

## Phase 2: Family Exploitation (iterations 16-40)

If one family type is winning (≥2 beats record):
1. Generate 3-5 variants within THAT family:
   - For Gaussian: vary μ spacing, σ values, weights
   - For B-spline: optimize control point magnitudes, adjust knots
   - For oscillatory: vary α amplitude, β frequency, γ decay rate
2. Probe all variants, evaluate top 2
3. Continue until: (a) stagnation (5+ iterations no improvement), or (b) max_iterations

## Phase 3: Crossed Experimentation (iterations 41-60)

If still stuck:
1. Try hybrid approaches: combine elements from 2 different families
2. Or switch to completely different paradigm (smooth → sharp or vice versa)

## Key Rules
- PARALLEL EXPLORATION from iteration 1: don't refine one type endlessly
- Use probes to filter: 30 probes = rank many variants cheaply
- Call generate_candidates EVERY 5 iterations OR when stuck
- Evaluate ONLY after probe ranking; evaluate top 3 only
- Track which family types work best; exploit winners
- If no family wins after 15 iterations: try a completely new paradigm
