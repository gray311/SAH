---
name: discovery-optimization
description: "Constructive search for Erd\u0151s step functions. Generate mathematically principled candidates, use probe for rapid screening, evaluate top candidates. Emphasize direct construction over hyperparameter tuning."
---

# Erdős Minimum Overlap - Constructive Search Strategy

## Problem Understanding

Minimize C5 = max_k ∫₀² h(x)(1-h(x+k)) dx
Subject to: h: [0,2] → [0,1], ∫h(x)dx = 1

The C5 bound comes from the autocorrelation of h(x). To minimize the maximum overlap, we want h to avoid being correlated with shifted versions of itself.

## Why Constructive Search Works

Gradient optimization from random initializations often finds suboptimal local minima.
The Erdős problem has a combinatorial nature: optimal solutions are often step-like with
specific structural patterns. Direct construction allows us to explore these patterns systematically.

## Search Strategy

### Step 1: Generate Multiple Constructions
Use construct_valid_step_function to create diverse candidates:
- bimodal: h concentrated in two narrow regions
- triangular/n-step: multi-level step patterns
- periodic: alternating on/off patterns
- Golomb-inspired: spacing to minimize overlaps
- asymmetric: break symmetry to reduce peak correlation

### Step 2: Rapid Screening with Probe
For each construction:
- Call probe_solution to check integral constraint and get approximate score
- Reject if integral is far from 1.0
- Note approximate C5 scores

### Step 3: Full Evaluation
Take top 1-3 constructions that pass screening:
- Implement as direct evaluation (no optimizer, just compute C5)
- Call evaluate_solution for exact scores
- Keep best results

### Step 4: Refine Promising Candidates
If a construction shows promise:
- Slight parameter adjustments (widths, positions, levels)
- Ensure integral constraint is satisfied
- Re-evaluate

## Key Constructions to Try

1. **Bimodal tight**: Two narrow peaks at optimal positions to minimize self-overlap
2. **Triangular n-step**: Multi-level pattern (0→α→1-α→0)
3. **Asymmetric peak**: Single peak shifted from center
4. **Periodic fractional**: On for fraction p of interval, off for 1-p
5. **Golomb ruler**: Peak positions inspired by optimal spacing

## Success Criteria

- combined_score > 1.0 (C5 < 0.380923)
- Document which construction achieved best result
- Use ~20 evals for evaluation, reserve probes for screening
