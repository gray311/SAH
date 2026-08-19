---
name: discovery-optimization
description: "C5 bound optimization using piecewise constant constructions.\nReduces search space from 800 continuous params to 10-20 breakpoint params.\nTargets combined_score > 1.0 by finding structurally-simple optimal solutions."
---

# C5 Bound Optimization: Piecewise Constant Strategy

THE CORE INSIGHT

The optimal step function h is NOT 800 independent parameters. It is a piecewise
constant function with FEW breakpoints (e.g., 5-20 intervals). Optimize those
directly, not via gradient descent on latent continuous parameters.

WHY THE SEED FAILS

- 800 latent params with sigmoid: overparameterized, hard to converge
- Adam optimization struggles in high-dimensional, non-convex landscape
- Multi-restart with same param count keeps finding same local optima

NEW STRATEGY: DIRECT PIECEWISE CONSTRUCTION

STEP 1: GENERATE CANDIDATES
Use construct_candidates to create explicit piecewise functions:
- Single block: h=1 on [0,1], h=0 elsewhere (satisfies integral=1)
- Two blocks: h=0.5 on [0,0.5] and [1.5,2], h=0 elsewhere
- Symmetric patterns: blocks centered at x=1
- Asymmetric patterns: explore [0,a], [b,c], [d,2] configurations

STEP 2: EVALUATE AND REFINE
- Evaluate each candidate directly (no gradient needed for initial scan)
- For promising candidates, refine breakpoint positions with local search
- Consider increasing discretization (500-1000 intervals) for final scoring

STEP 3: HYBRID APPROACH
- Use piecewise structure to initialize the seed's latent optimization
- Fix h values at breakpoints, optimize breakpoint positions
- Use the constraint integral=1 to adjust heights automatically

KEY CANDIDATES TO EXPLORE

1. SINGLE PEAK: h=1 on [0,1] -> c5 bound from correlation of step function
2. DOUBLE PEAKS: h=0.5 on two intervals of total length 2 -> spread the mass
3. THREE PEAKS: h approx 1/3 on three intervals of total length 3 -> even more spread
4. OFFSET PATTERNS: Break symmetry by using asymmetric intervals

EVALUATION BUDGET

- 30 evaluations total
- Spend 10-15 on candidate generation and initial evaluation
- Spend 10-15 on refinement of top candidates
- Goal: Find ANY solution with c5_bound < 0.38092303510845016

IMPORTANT

- COMPLETE REWRITES ARE REQUIRED - do not patch the seed's gradient descent
- USE construct_candidates to generate structured candidates
- EXPLORE FIRST, OPTIMIZE LATER - find good patterns before refining
- CONSTRAINTS: h in [0,1], integral=1, domain=[0,2]
