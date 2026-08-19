---
name: discovery-optimization
description: "Family exploration. Test piecewise linear, Gaussian mixtures, splines. Avoid re-running seed step patterns."
---

# Family Exploration Protocol

## Phase 1: Prototype New Families (iterations 1-12)
Select ONE family: Gaussian mixture (3 Gaussians), piecewise linear (5-7 knots), or spline. 
Call probe_family for fast prototype test. If probe >= 1.0, call evaluate_solution.

## Phase 2: Refine (iterations 13-24)
Generate 3 variants: perturb 20% parameters, adjust scale, symmetric vs asymmetric.
Probe all 3, evaluate best.

## Phase 3: Hybrids (iterations 25-30)
Try step+Gaussian tails. Probe 2, evaluate best, submit if c2 > record.

## Key Rules
- EXPLORE NEW FAMILIES, do not re-run seed step patterns
- PROBE FIRST: use probe_family before full eval
- Use 30 evals wisely: 1-2 per family
