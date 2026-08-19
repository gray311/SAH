---
name: discovery-optimization
description: "Step-function pattern mutation with convolution-aware analysis. Focus on asymmetric heights, multi-level structures, and localized features within the step-function family."
---

# C2 Maximizer: Step-Function Refinement Protocol

## Why Step Functions Work

Step functions create convolution peaks at specific locations while maintaining low ||f||_∞. 
The key is balancing the L2 norm (favoring spread) vs L∞ norm (favoring concentration).

## Mutation Strategy

### Phase 1: Analysis (Iteration 1)
1. Call analyze_convolution_patterns on the seed to understand current structure
2. Note: edge symmetry, height distribution, spacing ratios

### Phase 2: Targeted Mutations

**Mutation Type A: Asymmetric Height Adjustment**
- Make left/right step heights different (e.g., 1.50 → 1.55 left, 1.45 right)
- This breaks symmetry and may reduce constructive interference at center

**Mutation Type B: Multi-Level Enhancement**
- Add intermediate height levels between main steps (e.g., base=1.40, middle=1.80, top=2.00)
- Creates richer convolution structure

**Mutation Type C: Localized Bumps**
- Add small triangular/plateau bumps in unused regions
- Increases ||f★f||₂ without significantly affecting ||f★f||_∞

**Mutation Type D: Edge Refinement**
- Sharpen transition regions (narrower steps)
- Smooth transition regions (wider steps with gradients)

### Phase 3: Iteration

1. Generate 2-3 variants per mutation type
2. Use probe_solution to rank them (30 probes!)
3. Evaluate top 1-2 per type with evaluate_solution
4. If no improvement after 3 mutation types: restart from Phase 1 with fresh patterns

## Critical Rules

- NEVER exhaustively refine one variant - keep exploring new mutations
- Use probes to filter losers BEFORE full evaluation
- If stuck after 10 iterations, try COMPLETELY new step-function architectures
- Smooth functions (Gaussian, splines) are unlikely to beat the record - focus on steps
