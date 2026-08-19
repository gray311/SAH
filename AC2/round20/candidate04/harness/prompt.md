You are optimizing C2 = ||f*f||_2^2 / ((∫f)^2 ||f*f||_∞) for non-negative f:ℝ→ℝ.
Current best: 0.8962799441554086 (seed achieves combined_score=1.042, so it's already good).

CRITICAL: The seed uses FFT-based convolution with 600 intervals. Small changes to discretization,
integration method, or convolution precision can unlock improvements.

SEARCH STRATEGY (use all 30 evals):
PHASE 1 (iter 1): PRECISION TUNING
- Analyze current best's convolution profile using analyze_convolution_profile
- Try INCREASING num_intervals (800-1200) for better FFT resolution
- Probe all variants, evaluate top 2

PHASE 2 (iter 2-3): SHAPE REFINEMENT  
- If Phase 1 didn't beat record by 0.5%, try SMALL shape mutations:
  * Adjust step boundaries by ±2%
  * Tweaking heights by ±0.05
- Probe all, evaluate best

PHASE 3 (iter 4-5): ARCHITECTURE EXPANSION
- Only if stuck: add ONE new level to step function or switch to Gaussian mixture
- Evaluate top 1

RULES:
- Call probe_solution on ALL variants before any full eval
- NEVER waste evals on probe score < 1.0
- Use JAX array mutation (f.at[...] for in-place edits)
- Always call analyze_convolution_profile at start to diagnose
