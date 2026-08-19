Erdos C5 minimization: Find h:[0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h)=1 exactly, h in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving combined_score > 1.0 (c5_bound < 0.380923).

CRITICAL STRATEGY: DO NOT rely on long gradient training from seed hyperparameters.

STEP 1: GENERATE DIVERSE PATTERNS: Call smart_pattern_generator ONCE to get 3 valid,
integral-constrained initializations with precomputed c5_bound scores.

STEP 2: EVALUATE PROMISING PATTERNS: For any candidate with c5_bound < 0.378,
CALL evaluate_solution to verify with full 59000-step training.

STEP 3: SYSTEMATIC PATTERN VARIATION: If no success, generate more patterns with
different parameter combinations.

STEP 4: ONLY use gradient training as final refinement on promising candidates.

PATTERN FAMILIES TO EXPLORE:
- Golomb rulers: [0.0, 0.4, 0.8, 1.2, 1.6] or [0.0, 0.5, 1.0, 1.5]
- Bipartite: split at a=0.4, 0.45, 0.5, 0.55, 0.6
- Tri-modal: peaks at [0.3,1.0,1.7], [0.4,1.0,1.6], [0.45,1.0,1.55]
- Quadratic: parabolic mass distributions
- Multi-peak Gaussian: 4-5 narrow peaks at strategic positions

Use smart_pattern_generator's analytical FFT scoring to filter BEFORE any full eval.
Full evaluation is expensive - only evaluate when smart_pattern_generator shows promise.
