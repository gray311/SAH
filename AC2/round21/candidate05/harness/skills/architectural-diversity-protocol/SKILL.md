---
name: architectural-diversity-protocol
description: Step-function architecture search. Generate diverse variants (varying intervals, peaks, asymmetries), probe to screen, then refine winners. Structural innovation beats parameter tuning.
---

# C2 Maximizer: Architectural Diversity Protocol

## Core Principle
The seed step patterns are trapped in local optima. Generate NEW architectures, not just refine
existing ones. Vary interval counts, peak configurations, and asymmetries.

## Phase 1: Architecture Generation (iterations 1-10)

Step 1: Generate Diverse Architectures
- Call generate_step_variants to create 4-6 structurally different functions
- Vary: number of intervals (200/400/800/1200), peak count (1/2/3), asymmetry (left/right/center)
- Combine patterns: e.g., pattern 9 (asymmetric multi-level) + pattern 10 (wide base)

Step 2: Aggressive Probing
- Call probe_solution on ALL variants (30 probes = screen 10-15 architectures)
- Rank by probe score
- NEVER evaluate before probing - use probes to filter

Step 3: Select Top Candidates
- Evaluate top 2 by probe score
- If both underperform: generate different architectural styles (e.g., try 2-peak instead of 1-peak)

## Phase 2: Gradient Fine-Tuning (iterations 11-20)

Step 1: Refine Best Architecture
- Take highest-scoring variant from Phase 1
- Compute @jax.grad(-c2_ratio)

Step 2: Gradient Variants
- Variant A: param = param + 0.05 * gradient
- Variant B: Random 10% perturbation (Gaussian noise)

Step 3: Probe and Evaluate
- Probe both, evaluate best
- Continue refinement or switch to Phase 3

## Phase 3: Hybrid Constructions (iterations 21-30)

Step 1: Advanced Combinations
- Step + envelope: f(x) * exp(-x^2/100)
- Multi-scale steps: Fine steps on coarse support
- Spline approximation to step pattern

Step 2: Generate 3 Hybrids, Probe All, Evaluate Best
- Submit if beats record

## Key Rules
- generate_step_variants creates STRUCTURAL diversity
- probe_solution: screen 10-15 variants before any eval
- Structural innovation > parameter tuning
- If stuck at iteration 10+: try completely different architectures
