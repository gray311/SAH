---
name: family-exploration-protocol
description: Prototype and refine new function families. Avoid re-running seed step patterns.
---

# Family Exploration Protocol

## Phase 1: Prototype (iterations 1-12)
Select ONE family: Gaussian mixture, piecewise linear, or spline. Call probe_family. If probe >= 1.0, evaluate.

## Phase 2: Refine (iterations 13-24)
Generate 3 variants per family. Probe all, evaluate best.

## Phase 3: Hybrids (iterations 25-30)
Try step+Gaussian tails. Probe 2, evaluate best, submit.

## Key Rules
- EXPLORE NEW FAMILIES
- PROBE FIRST
- Use 30 evals wisely
