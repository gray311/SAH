---
name: discovery-optimization
description: "Refine seed's multi-level step patterns through systematic perturbations. Pick best existing pattern, then apply gradient-like changes (height \u00b10.05-0.15, position \u00b12-5%, asymmetry, width adjustments). One change per edit. Learn and iterate toward beating 1.03663."
---

# C₂ Pattern Refinement Protocol

## Core Strategy
The seed has 13 optimized step patterns. Don't invent new patterns. Instead: find the best one and refine it systematically.

## Step 1: Pattern Selection (evals 1-2)
Examine all 13 patterns. Prioritize:
- Pyramid patterns (idx 2,4,6,7,8,9,10,11,12)
- Patterns with high central peaks (1.50+)
- Well-structured multi-level patterns

Pick ONE as your base. Study its structure.

## Step 2: Systematic Perturbation
Make ONE small change at a time:

**Height Adjustment**:
- If central peak = 1.90, try 1.95, 2.00, 1.85
- If side peak = 0.80, try 0.85, 0.75, 0.90

**Position Shift**:
- If peak spans [0.30n, 0.70n], try [0.28n, 0.72n]
- If gap is 0.20n, try 0.18n, 0.22n

**Asymmetry**:
- Heights [0.80, 2.00, 0.80] → [0.78, 2.05, 0.82]
- Heights [0.90, 1.90, 0.90] → [0.88, 1.95, 0.92]

**Width**:
- Expand/narrow peak region by ±2-5%
- Wider peaks may lower ||f★f||∞

## Step 3: Iteration Loop
1. Modify ONE parameter
2. Evaluate
3. If score ↑: modify SAME parameter in same direction or adjacent parameter
4. If score ↓: try different parameter or reverse direction
5. Repeat

## Step 4: If Plateau (after eval 15-20)
- Mirror the pattern: swap left/right
- Add an intermediate level between existing levels
- Reduce number of levels by 1
- Scale all peaks up/down by 0.95 or 1.05

## Success Criteria
- Beat 1.03663
- Document which pattern and which modifications worked
