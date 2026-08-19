---
name: architectural-search
description: Guide exploration across function architectures. Use when current pattern class fails to improve.
---

# Architectural Search for C₂ Optimization

## When to Use
- Current architecture stagnant for 8+ iterations
- Parameter tweaking not yielding improvements
- Need fundamentally new function class

## Architecture Classes to Explore
1. **Asymmetric Bimodal**: Two distinct peaks at different heights
2. **Trimodal Plateau**: Three regions with central plateau
3. **Logarithmic Steps**: Steps spaced by log scale
4. **Narrow Peaked Wide**: Very narrow high peaks with wide shoulders
5. **Flat Top Asymmetric**: Flat-topped with asymmetric sides

## Search Protocol
1. Call analyze_step_params to assess current architecture
2. If no improvement in 8 iterations, call try_new_architecture
3. Generate 5-10 architectural variants
4. Probe all variants (3-5 probes each)
5. Evaluate single best variant
6. If improvement, refine; if not, try different architecture class

## Key Insight
The optimal C₂ function may require architectural diversity, not just parameter tuning.
Broad exploration beats careful fine-tuning when current class fails.
