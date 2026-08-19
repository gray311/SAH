---
name: parallel-exploration-playbook
description: Execute parallel exploration across multiple function families with probe-driven filtering.
---

# Parallel Exploration Playbook for C₂ Maximization

## Why This Works
The step-function record (1.04199) is a LOCAL optimum. Different function families have different optima. By exploring families in PARALLEL, you maximize chances of finding a better global optimum.

## The 30-Probe Strategy
You have 30 full evaluations. Use them WISELY:
- 30 probes to filter 15+ candidates across families
- 3 evaluations on the best probe-scoring candidates
- Repeat until budget exhausted

## Iteration Loop (repeat 10-15 times per 30-probe cycle)

### Cycle Start: Diverse Generation
1. Call generate_candidates to get 3-5 proposals from DIFFERENT families:
   - Gaussian mixtures: smooth multi-peaked functions
   - B-spline basis: flexible control points with softplus
   - Oscillatory decay: (1 + α cos(βx)) * exp(-γ|x|)
   - Piecewise-linear: vertices with optimized heights
   - Multi-level improved steps: asymmetric patterns

2. Optionally call diversity_analyzer to ensure you're not stuck in one family

### Probe Phase
3. Call probe_solution for EVERY candidate (use all 30 probes across the cycle)
4. Rank by probe score
5. Discard any with probe score < 1.04199 (current best)

### Evaluate Phase
6. Select top 3 by probe score
7. Call evaluate_solution for each (uses 3 evaluations)

### Decision
8. If ANY evaluation beats 1.04199:
   - That's your new champion!
   - Call generate_candidates for fresh ideas (don't over-refine)
   - Optionally refine the winner SLIGHTLY (one tiny mutation)
9. If NONE beat the record:
   - Generate a NEW set from different families
   - Try hybrids: "Gaussian with step edges", "oscillatory steps"
   - Vary parameter ranges (wider oscillations, different decays)

## Key Principles
- PARALLEL > SEQUENTIAL: Don't spend 5+ iterations on one family
- PROBE FIRST: Never evaluate without probing
- DIVERSIFY: If diversity_analyzer shows low diversity, force new families
- HYBRIDIZE: Combine successful elements from different families
- QUICK DECISIONS: After 3 evaluations without improvement, generate new ideas
