---
name: pattern-optimization-strategy
description: Strategy for optimizing Erdos patterns - use pattern_modifier to create variants, then train with 59000 steps. Focus on Golomb (12) and Tri-modal (14) patterns.
---

# Pattern Optimization Strategy for Erdos Problem

## Understanding the Patterns

The seed's _get_best_initialization generates 15 patterns.
Patterns 0-4, 7 are noisy/random. Patterns 5-14 are structured.

Best patterns to focus on:
- Pattern 12: Golomb ruler (5 marks at optimal spacing)
- Pattern 14: Tri-modal (3 peaks at 0.4, 1.0, 1.6)
- Patterns 5, 6, 8, 9, 13: Bipartite (threshold-based)

## Using pattern_modifier

1. CALL pattern_modifier with pattern_id=12, mod_type='narrow_peaks', mod_value=0.05
   - This creates Golomb with narrower peaks (width 0.05 instead of 0.1)

2. CALL pattern_modifier with pattern_id=14, mod_type='shift_peaks', mod_value=0.2
   - This shifts the tri-modal peaks

3. EDIT the EVOLVE-BLOCK to update the pattern parameters
   - Change the marks array, threshold 'a', or peak positions

4. CALL evaluate_solution to train the new variant for 59000 steps

## Parameter Tweaking Guide

### Golomb Pattern (pattern 12)
- Narrow peaks: mod_value=0.05-0.08 (decreases overlap)
- Add marks: Edit code to add more marks to marks array
- Shift marks: Edit code to change mark positions

### Tri-modal Pattern (pattern 14)
- Narrow peaks: mod_value=0.08-0.12 (decreases overlap)
- Shift peaks: Edit code to change [0.4, 1.0, 1.6]
- Add/remove peaks: Edit code to modify peaks array

### Bipartite Pattern (patterns 5,6,8,9,13)
- Adjust threshold: mod_type='adjust_threshold', mod_value=0.55
- Shift the split point

## Workflow

1. Pick a pattern_id (recommend 12 or 14)
2. Use pattern_modifier to generate a variant
3. EDIT the code with new parameters
4. CALL evaluate_solution
5. Check combined_score > 1.0? If yes, FINISH.

## Important

- Each evaluation trains for 59000 steps. Be strategic.
- Start with small modifications (mod_value ~ 0.5-0.8)
- Track which patterns work best
