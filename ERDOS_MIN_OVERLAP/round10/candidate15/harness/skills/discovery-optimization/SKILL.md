---
name: discovery-optimization
description: "Structural initialization innovation for Erdos problem. Focus on creating new initialization patterns with different mathematical structures (piecewise, multi-level, shifted/scaled) rather than hyperparameter tuning. Use probe for constraint checking."
---

# Erdos Minimum Overlap - Structural Initialization Strategy

## Why Hyperparameter Tuning Failed
The seed optimizer uses Adam (LR=0.007, penalty=60, 59000 steps) but gets stuck in local minima.
Small hyperparameter changes don't change the optimizer's fundamental ability to find good solutions.
**The solution requires BETTER initializations** with structures that explore different regions of the solution space.

## Strategy: Structural Innovation

### Phase 1: Add New Pattern Families (Primary Focus)
Edit _get_best_initialization() to add NEW initialization families:

1. **Shifted/Scaled Patterns**: For each existing pattern, create variants:
   - scale_factor: 0.5, 0.7, 1.0, 1.3, 1.5, 2.0
   - shift: 0, 0.25, 0.5, 0.75, 1.0

2. **Piecewise Constant with 3-4 Levels**:
   - Divide [0,2] into 3-4 intervals with different constant values
   - Try ratios like: 0.6:0.2:0.2, 0.5:0.3:0.2, 0.7:0.1:0.2, etc.
   - Ensure integral = 1 after sigmoid transformation

3. **Width-Optimized Peaks**:
   - Instead of fixed widths, try different peak widths: 0.1, 0.15, 0.2, 0.25, 0.3
   - For bimodal: peaks at (α, 1-α) with width w
   - Try α in {0.2, 0.25, 0.3, 0.35} and w in {0.1, 0.15, 0.2}

4. **Asymmetric Constructions**:
   - Three-region: low on [0,a], high on [a,1-a], low on [1-a,2]
   - Try a in {0.2, 0.25, 0.3, 0.35, 0.4}
   - Try different high/low ratios

### Phase 2: Evaluation Strategy
1. For each new pattern family, generate 5-10 variants
2. Use **probe_solution** to quickly screen:
   - Check if sigmoid(latent) is in [0,1]
   - Check if ∫h(x)dx ≈ 1 (within 0.05 tolerance)
3. Call **evaluate_solution** on the BEST variant of each family
4. Keep the best result and continue iterating

### Phase 3: Refinement (if needed)
If you find a promising pattern but not quite optimal:
- Use smaller amplitude noise for fine-tuning
- Try combining elements from multiple good patterns

### Success Criteria
- combined_score > 1.0 (c5_bound < 0.380923)
- Document the winning initialization pattern
