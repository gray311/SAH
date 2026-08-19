---
name: discovery-optimization
description: "Incremental optimization of C\u2082 via systematic perturbation of seed patterns.\nFocus on extracting features from working patterns and recombining them."
---

# C₂ Optimization via Feature Extraction and Recombination

## Core Strategy

The seed program has 13 pre-tuned step patterns achieving ~1.036. Small mutations won't help.
Instead: extract features from successful patterns and recombine them.

## Phase 1: Feature Analysis (first iteration only)

1. Call analyze_pattern to get all 13 patterns' heights and structures
2. Identify patterns with highest diversity in features (heights, intervals)
3. Note which patterns use similar feature combinations

## Phase 2: Incremental Mutation

For each iteration, do ONE of:

- **Height perturbation**: Change one height by ±10% (e.g., 1.40 → 1.54 or 1.26)
- **Interval shift**: Move one interval boundary by ±5% of the domain
- **Feature recombination**: Take heights from pattern A, combine with interval structure from pattern B
- **Asymmetric variant**: Mirror one pattern but shift the center

DO NOT:
- Change 3+ parameters at once
- Create patterns with >15 levels (too complex)
- Delete existing patterns

## Phase 3: Evaluation and Drilling

1. Edit ONE pattern with ONE change
2. Evaluate immediately
3. If improved: DO MORE mutations on this SAME pattern (drill down)
4. If not improved after 3 evals: switch to a DIFFERENT base pattern
5. Track which pattern class performs best

## Phase 4: Convergence

- If you find a pattern that improves repeatedly, keep mutating it
- If all patterns plateau, try feature recombination
- Report the best C₂ and the pattern modifications that achieved it

Key principle: SMALL, SYSTEMATIC CHANGES beat radical redesigns on this task.
