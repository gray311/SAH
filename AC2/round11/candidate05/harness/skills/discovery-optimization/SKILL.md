---
name: discovery-optimization
description: "Incremental parameter refinement for C2 maximization. Systematically vary heights, intervals, and widths of existing step patterns with small, targeted edits. Evaluate each variant and iterate within successful pattern classes."
---

# C2 Optimizer: Parameter Refinement Protocol

## Core Principle

The 13 seed step patterns are already structurally sound. Small parameter variations within each pattern can improve C2. Focus on incremental refinement.

## Phase 1: Select a Pattern Class

Pick ONE of the 13 seed patterns that showed promise. Focus on its specific structure.

## Phase 2: Systematic Parameter Variation

Vary ONE parameter at a time:

**Height Tuning:**
- If a peak is at 1.40, try 1.42, 1.38, 1.45, 1.35
- Test 3-5 height variants per peak before moving on

**Interval Positioning:**
- Shift interval boundaries by +/-5% (e.g., if start is 0.25*n, try 0.225*n and 0.275*n)
- Small shifts can change convolution interference patterns

**Width/Level Count:**
- For 2-level patterns, try adding a third intermediate level
- For 4+ level patterns, try merging adjacent levels or splitting one

## Phase 3: Evaluation Discipline

1. Evaluate ONE variant per iteration
2. If score improves: continue refining that variant
3. If score worsens: undo change, try a different variant
4. After 3 failed attempts on a parameter: move to a different parameter

## Phase 4: Pattern Migration

If stuck after 5-6 iterations on one pattern:
- Select a DIFFERENT seed pattern to refine
- Do NOT combine patterns yet - master one class first

## Key Principles

- Incremental: Change 1-2 parameters per edit, never 5+
- Persistent: Spend 3+ evaluations on a pattern class before abandoning
- Focused: One pattern at a time, not multiple competing ideas
