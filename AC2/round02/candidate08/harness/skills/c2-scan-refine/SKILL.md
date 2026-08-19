---
name: c2-scan-refine
description: Enforce scan-refine protocol - use scan_representations to probe 4+ function classes, then refine top 2-3 with full evaluations. Prevents tunneling.
---

# C2 Scan-Refine Protocol

## Objective
Maximize C2 > 0.8963 by exploring DIVERSE function representations.

## Phase 1: Scan
Call scan_representations() at start. Probes: 4 step, 3 pwlinear, 3 Gaussian, 2 exponential.

Analyze results:
- If step wins: Refine with more levels, different supports
- If Gaussian wins: Refine with more components
- If pwlinear wins: Refine with more intervals
- If exp wins: Try other forms too!

Probe budget: ~18 total

## Phase 2: Refinement (3-5 full evals)
For TOP 2-3 REPRESENTATIONS:
1. Increase intervals/parameters 2-3x
2. Multi-start: 3 random initializations each
3. Fine-tune: LR, steps, stagnation
4. Use probes to rank before full evals

## Phase 3: Ensemble and Innovation
- Weighted averages
- Analyze structural properties
- Design inspired variants

## Critical Rules
- DO NOT spend all 20 evals on one class
- DO NOT just tune hyperparameters
- DO diversify across 4+ classes
- DO use scan_representations
- DO reserve 4-5 evals for winners

## Recovery
- If stuck: Try different class
- If evals low: Consolidate on best
- If errors: Fix immediately
