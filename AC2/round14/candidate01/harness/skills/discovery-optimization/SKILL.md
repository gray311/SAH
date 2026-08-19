---
name: discovery-optimization
description: "Structurally-guided C\u2082 maximization. Use convolution analysis to understand successful patterns, then apply targeted mutations with probe-based filtering."
---

# C₂ Maximizer: Structurally-Guided Mutation Protocol

## Core Principle

Step functions achieve high C₂ because their convolutions have concentrated peaks and controlled tails. Understand this structure first, then mutate systematically.

## Phase 1: Structural Analysis (Iterations 1-3)

1. Call analyze_convolution_structure ON the current best function
2. Extract key properties: peak locations, symmetry, tail decay, relative heights
3. Note which structural features likely contribute to high C₂

## Phase 2: Targeted Mutation Generation

Generate mutations based on structural insights:

**Mutation Type A: Height Perturbation**
- Increase highest peaks by 0.05-0.15, decrease others proportionally
- Try: concentrate mass at critical convolution peaks

**Mutation Type B: Width Adjustment**
- Expand core intervals by 5-10% (increases L2 norm without drastically increasing L∞)
- Contract edge intervals by similar amounts
- Maintain total mass roughly constant

**Mutation Type C: Symmetry Breaking**
- Take symmetric pattern, make heights slightly asymmetric (e.g., 1.40, 1.48, 1.32)
- Shift left/right portions relative to each other by 2-3%

**Mutation Type D: Localized Enhancement**
- Add a small bump (height 0.3-0.6, width 5-15 intervals) near convolution peaks
- Place at positions where convolution naturally has secondary peaks

**Mutation Type E: Multi-Level Refinement**
- If 2-level, try 3-level with intermediate height
- Fine-tune all level heights (not just core vs wings)

## Phase 3: Probe-Based Filtering

1. For EACH mutation variant, call probe_solution IMMEDIATELY
2. You have 30 probes - use them to rank ALL variants
3. Select top 3-5 by probe score for full evaluation
4. SKIP full eval if probe score < current best (probe is a good predictor here)

## Phase 4: Full Evaluation & Iteration

1. Evaluate top 3-5 variants with evaluate_solution
2. If improvement: analyze new best, generate more mutations in same pattern
3. If no improvement after 3 mutation types: try different type
4. If 10+ iterations with no improvement: switch to completely new architecture

## Phase 5: Architecture Switching (Last Resort)

If stuck, try: Gaussian mixtures (smooth multi-peaked), B-splines (flexible smooth), or oscillatory decay functions.

Key: STRUCTURAL UNDERSTANDING + PROBE FILTERING = EFFICIENT SEARCH. Don't refine one type exhaustively.
