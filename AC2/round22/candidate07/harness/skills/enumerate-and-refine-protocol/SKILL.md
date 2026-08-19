---
name: enumerate-and-refine-protocol
description: Systematically enumerate diverse step function architectures, probe filter, then refine best.
---

# Two-Phase Architecture Search Protocol

## Phase 1: Architecture Enumeration (iterations 1-20)

1. Call enumerate_patterns with different configs:
   - Different resolutions: 400, 600, 800 intervals
   - Different shapes: single/trapezoid/Gaussian-like/two-peak
   - Different base styles: flat_spike/flat_double_spike

2. Probe ALL 8-12 variants (use 20 probes total)

3. Rank by probe score, evaluate TOP 2

4. If best beats seed (combined > 1.042): switch to Phase 2
   If neither beats seed: try different configurations

## Phase 2: Gradient Refinement (iterations 21-30)

1. Use JAX autodiff for gradient ascent
2. Take step: new_param = param + 0.08 * gradient
3. Probe both ascent/descent, evaluate best

## Key Rules
- Enumerate ARCHITECTURES first - seed patterns may be suboptimal
- Use probes to filter 10+ candidates before evals
- Try multiple discretization resolutions
- If stuck at iteration 15+: try new base_style or peak_shapes
