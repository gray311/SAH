---
name: incremental-c2-optimization
description: Systematic C₂ optimization through incremental perturbation of seed patterns. Focus on small, surgical edits and feature recombination rather than radical redesign.
---

# Incremental C₂ Optimization Protocol

## Understanding the Task

You have 13 pre-optimized step patterns achieving ~1.036. The current harness failed
because it asked for "new architectures" - but the answer is better optimization of
existing patterns through systematic, small mutations.

## Strategy: Feature Extraction and Recombination

### Step 1: Analyze (one-time)
- Call analyze_pattern to understand all 13 patterns
- Note the range of heights (0.60 to 2.30) and pattern types
- Identify patterns with unique features (e.g., pyramid, asymmetric multi-level)

### Step 2: Mutation Types

Choose ONE mutation per iteration:

**A. Height Perturbation**: Change one height by ±10%
- 1.40 → 1.54 or 1.26
- 2.10 → 2.31 or 1.89
- Try both increase and decrease for each pattern

**B. Interval Adjustment**: Shift one interval by ±5%
- int(0.25*n) → int(0.24*n) or int(0.26*n)
- Test whether moving the peak slightly left/right helps

**C. Feature Recombination**: Mix features from different patterns
- Take central heights from pyramid pattern, combine with intervals from staircase
- Use multi-level structure from pattern 3 with heights from pattern 11

**D. Asymmetric Variant**: Break symmetry of symmetric patterns
- Pattern 3 (0.90, 1.90, 0.90) → try (0.90, 2.00, 0.85)
- Keep central high, adjust sides slightly differently

### Step 3: Evaluation Protocol

1. Edit ONE pattern with ONE change
2. Call evaluate_solution immediately
3. Record the result
4. If improved: DO MORE mutations on this SAME pattern (drill down)
5. If no improvement after 3 consecutive evals: switch base pattern

### Step 4: Tracking

Maintain mental model of:
- Which base patterns have shown promise
- Which mutation types work (height vs interval vs recombination)
- The current best C₂ and what produced it

## Key Principles

- SMALL changes: ±10% height, ±5% intervals
- ONE change at a time: don't mutate multiple parameters
- DRILL DOWN: if something improves, keep mutating that same pattern
- SYSTEMATIC: try height increases, then decreases, then intervals
- RECOMBINE: mix features from successful patterns
