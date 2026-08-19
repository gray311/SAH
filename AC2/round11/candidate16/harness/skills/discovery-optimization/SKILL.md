---
name: discovery-optimization
description: "Systematic pattern mutation for C\u2082 maximization. Use analyze_current_pattern to examine the current best pattern's structure, then apply targeted mutations (height, position, width adjustments). Use c2_analyze for feedback before full evaluation."
---

# C₂ Maximizer: Systematic Pattern Mutation Protocol

## Core Principle

Don't generate patterns from scratch. Mutate the current best pattern systematically.

## Phase 1: Identify Current Best

1. Call analyze_current_pattern to see all 13 patterns' structures
2. Note which pattern the evaluator currently uses (look for comments or score tracking)
3. Extract its exact height values and interval positions

## Phase 2: Targeted Mutations

Try these mutation types in order:

**A. Height Adjustment** (most promising)
- Change each step's height by ±10%, ±5%, or ±2%
- Focus on the tallest peak (often 1.8-2.1 in seed): try 1.7, 1.8, 1.9, 2.0, 2.1
- Also tune side peaks: 1.2 → 1.1, 1.3 → 1.25

**B. Position Shifting**
- Move peak boundaries by 1-2 intervals: int(0.25*n) → int(0.26*n) or int(0.24*n)
- Make central peak narrower: extend by ±5% instead of ±25%

**C. Width/Spacing Adjustment**
- Compress or expand the main peak region by 10%
- Adjust gap between peaks

**D. Wing Addition/Removal**
- Add small wings: new steps with 5-8% height at ±20% from edges
- Remove small wings if they inflate ||f★f||∞

## Phase 3: Analyze Before Evaluating

1. Call c2_analyze on your mutated pattern
2. Check: Did L2 norm increase? Did infinity norm stay stable or decrease?
3. Only call evaluate_solution if c2_analyze shows potential

## Phase 4: Iterate or Pivot

- If mutation improves: drill deeper with finer adjustments (±2%, ±1 interval)
- If stuck for 5 iterations: try a different mutation strategy (e.g., heights → positions → wings)
- Keep trying mutations until you beat 1.03663

## Example Mutation Workflow

1. analyze_current_pattern → see pattern 12 has heights [0.70, 1.50, 2.10, 1.50, 0.70]
2. c2_analyze → shows L2=0.85, inf=2.3, ratio=1.036
3. Mutate: change center to 2.20 → c2_analyze → L2=0.87, inf=2.25, ratio=1.042 (promising!)
4. evaluate_solution → 1.045 (NEW RECORD!)
5. Drill: try center=2.25, 2.30 → find optimum at 2.28
