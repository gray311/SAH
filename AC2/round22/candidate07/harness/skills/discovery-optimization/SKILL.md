---
name: discovery-optimization
description: "Architecture enumeration for step-function optimization. Systematically try diverse step-function families (different window shapes, multi-peaks, discretizations) before refinement."
---

# C2 Maximizer: Two-Phase Architecture Search

## Phase 1: Systematic Enumeration (iterations 1-20)

1. Call enumerate_patterns to generate diverse step functions:
   - Try different total intervals (600, 400, 800)
   - Try different peak shapes: (a) single wide, (b) two asymmetric peaks, (c) trapezoid, (d) Gaussian-like bell, (e) split multi-peak
   - Try different base patterns: wide flat + narrow spike, or two narrow spikes on flat base
   - Generate 8-12 variants with PROBABILISTIC choices (temperature=0.8)

2. Probe ALL generated variants (use 20 probes)

3. Evaluate TOP 2 variants by probe score

4. If both beat seed (combined > 1.042): switch to Phase 2 with best one
   If neither: try different window shapes

## Phase 2: Gradient Refinement (iterations 21-30)

1. Use JAX autodiff: @jax.grad on -c2_ratio
2. Take gradient ascent step with learning_rate=0.08
3. Probe both ascent and descent variants
4. Evaluate best

## Key Rules
- Enumerate architectures first - don't waste evals refining weak seeds
- Use probes to filter 10+ candidates before any full eval
- Try multiple discretization resolutions (400, 600, 800 intervals)
- If stuck: call enumerate_patterns with DIFFERENT peak_shapes parameter
