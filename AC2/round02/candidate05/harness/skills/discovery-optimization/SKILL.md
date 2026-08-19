---
name: discovery-optimization
description: "Optimize C2 function discovery. Must make structural changes (not parameter tweaks), use probe_solution for ranking (~15 probes per variant), switch representations after stagnation. Priority: piecewise-constant, Gaussian mixtures, multi-scale. Budget: 20 evals. Probes filter candidates before eval."
---

# C2 Function Discovery - Structural Change Strategy

## Objective
Beat C2 = 0.8963 record. The seed (piecewise-linear) achieves ~0.8963 * 1.026 = 0.919. We need structural innovation.

## Core Principle
**Structural over Incremental**: Parameter tuning alone cannot escape local optima. Change function REPRESENTATION, not just parameters.

## Exploration Protocol

### Phase 1: Rapid Representation Sweep (Use Probes!)
Test these FIVE classes, 10-15 probes each:

1. **Piecewise-Constant (Step Functions)**
   - Parameterize: Array of N bin heights
   - Variants: Symmetric, asymmetric, support shifts
   - Why: Current record-holder

2. **Gaussian Mixtures**
   - Parameterize: K means, variances, weights
   - Ensure: f(x) >= 0 (use exp/softplus)
   - Why: Smooth, often optimal for integral problems

3. **Multi-Scale Approach**
   - Coarse: num_intervals=50-100, optimize
   - Fine: Refine with num_intervals=200-400
   - Why: Escapes coarse grid local optima

4. **Piecewise-Linear Variants**
   - Seed uses this. Try: more intervals (400-800), triangular peaks, multi-modal
   - Why: Continuity helps some problems

5. **Asymmetric/Shifted Support**
   - Shift support to [0.1-0.5], [0.25-0.75], etc.
   - Vary left/right weights
   - Why: Symmetry may not be optimal

### Phase 2: Budgeted Evaluation
- Evaluate ONLY top 3-5 by probe score
- Each eval = confirm best variant, not exploration
- If validity=0, fix immediately, don't re-evaluate same code

### Phase 3: Stagnation Response
- Track last 5 eval scores
- If all within 1e-4 of each other for 3+ iterations: FORCE representation switch

## Tool Usage Strategy
- probe_solution: 10-15 per function class (50 total probes = cheap)
- evaluate_solution: 3-5 total (budget constraint)
- edit_solution: Always substantive (change intervals, class, or init pattern)
- finish: When evals=0 or no improvement in 5 iterations

## Decision Tree
1. What representation am I using?
2. Has this yielded improvement?
3. If YES and score stable: Switch to next class in priority order
4. If NO: Try parameter variation within this class (1-2 probes)
5. Always document which class/variant you're testing
