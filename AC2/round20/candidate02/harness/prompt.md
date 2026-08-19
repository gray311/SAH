You are optimizing C2 = ||f*f||_2^2 / ((∫f)^2 ||f*f||_∞) for non-negative functions.
Current best: 0.8962799441554086 (achieved by step functions with specific patterns).

CRITICAL: The executor is a HIGH-QUALITY STEP-FUNCTION OPTIMIZER. Do NOT try Gaussian mixtures, B-splines, or oscillatory functions - the EVOLVE-BLOCK only supports step patterns.

STRATEGY - STEP-PATTERN OPTIMIZATION WITH TAIL EXPLORATION:

PHASE 1 (iterations 1-20): PATTERNS + TAIL EXPLORATION
1. Call analyze_step_patterns ON the current best to understand its step structure
2. Generate 3-5 VARIANT step patterns with DIFFERENT TAIL BEHAVIORS (longer support, asymmetric tails)
3. Call probe_solution on ALL variants (use all 30 probes to explore many variants)
4. Evaluate TOP 2 by probe score - ONLY if probe >= 1.0
5. If no improvement after 10 iterations: generate NEW patterns with EXTENDED TAILS (support [-4, 4] instead of [-3, 3])

PHASE 2 (iterations 21-40): FOCUSED REFINEMENT
1. Take best pattern from Phase 1
2. Generate 3 variants with SMALL mutations: adjust one interval boundary by ±3%, adjust one height by ±0.15
3. Probe all, evaluate top 1
4. If no improvement after 5 iterations: return to Phase 1 with DIFFERENT tail strategies

KEY RULES:
- Stay in step-function space - it works! The seed's 1.042 score proves it's on the right track
- Use probes aggressively: 30 probes to explore 15-20 variants before any full eval
- NEVER generate non-step architectures (Gaussian, B-spline, oscillatory)
- Always call analyze_step_patterns at iterations 0, 8, and when stuck
- Focus on TAIL BEHAVIORS: longer support, asymmetric decay, multi-peak structures
