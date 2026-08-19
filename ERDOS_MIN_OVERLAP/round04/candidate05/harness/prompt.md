You are an expert in harmonic analysis and the Erdős minimum overlap problem.

Target: Find a step function h: [0,2]→[0,1] with integral(h)=1 that minimizes
max_k ∫ h(x)(1-h(x+k)) dx.

CRITICAL INSIGHT: The optimal solution is a DISCRETE STEP FUNCTION with sharp transitions.
Smooth/Gaussian constructions are INCORRECT for this problem.

The seed program already has good initialization patterns - you need to:
1. USE HEAVISIDE/RECTANGULAR STEPS, not smoothed Gaussians
2. Enforce integral constraint MORE strictly during optimization
3. Try BROAD bimodal patterns (mass split evenly between two wide bands)

Strategy:

Phase 1 - Generate HARD step function initializations:
- Use Heaviside steps at strategic positions
- Create bimodal rectangles with TWO flat regions (high h) and TWO flat regions (low h=0)
- Ensure integral exactly equals 1 by adjusting widths/heights

Phase 2 - Optimize with AGGRESSIVE constraint enforcement:
- Phase 1: 10000 steps, lr=0.01, penalty=100000 (tight constraint)
- Phase 2: 20000 steps, lr=0.005, penalty=500000 (very tight)
- Monitor constraint violation and adjust if > 0.001

Phase 3 - Quick probe then confirm:
- Use probe_solution to rank all candidates
- Only full evaluate on top 2 that beat seed score

EVOLVE-BLOCK changes needed:
- Replace Gaussian constructions with sharp Heaviside/rectangular steps
- Add phase-based training loop with adaptive penalty
- Add constraint enforcement checks after each phase
- Start with a "wide bimodal" initialization: h=1 on [0,a] ∪ [b,2] with appropriate widths

Target: combined_score > 1.0 (c5_bound < 0.380923)
