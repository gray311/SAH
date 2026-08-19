---
name: step-function-exploration
description: Systematically explore step-function space before trying smooth functions.
---

# Step-Function Exploration Protocol for C2 Maximization

## Core Principle
Step functions are NOT trapped! The seed's 5 patterns are just starting points.
Exhaustively explore step-function space (3-7 levels, various heights, asymmetries)
BEFORE trying smooth functions.

## When to Generate Step Variants
1. At iteration 0: generate initial diverse step patterns using generate_step_variants
2. After each full eval: if no improvement, generate NEW step families
3. At iteration 15: if no improvement, try FRACTAL/MIRROR/CLUSTERED patterns
4. ONLY at iteration 20+ with no step improvements: try smooth functions

## Step Pattern Families (rotate through these)

Family A: Level Count Variation
- 3 levels: low-high-low (asymmetric)
- 4 levels: low-medium-high-low
- 5 levels: low-medium-high-medium-low
- 6-7 levels: fine-grained multi-level

Family B: Height Range Variation
- Heights [0.5, 1.0]: conservative, smooth transitions
- Heights [1.0, 2.0]: moderate peaks
- Heights [1.5, 3.0]: aggressive peaks (test limits)

Family C: Asymmetry
- Left-heavy: high levels on left side
- Right-heavy: high levels on right side
- Centered: symmetric around middle
- Biased-center: slight offset from center

Family D: Clustered Peaks
- 2-3 high peaks with low valleys between
- Mimics multi-modal distributions
- Test with 2 peaks, 3 peaks, 4 peaks

Family E: Fractal-like Patterns
- Self-similar: large-scale steps with fine-scale sub-steps
- Multiple scales: 10% intervals at coarse scale, 1% at fine scale

## Execution Flow
1. Call generate_step_variants at iteration 0 for diverse patterns
2. Call probe_solution on ALL candidates (5-8 variants)
3. Call evaluate_solution on TOP 2 by probe score
4. If no improvement: call generate_step_variants again with new families
5. Continue until iteration 15 or improvement
6. Only at iteration 20+ with no improvements: try smooth functions

## Key Rule
STEP FUNCTIONS FIRST: exhaustive search before trying smooth functions.
Smooth functions have higher numerical error and should be last resort.
