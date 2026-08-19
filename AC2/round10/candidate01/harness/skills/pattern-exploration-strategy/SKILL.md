---
name: pattern-exploration-strategy
description: Exploration strategy for C2 optimization. Generate diverse patterns, probe rank, evaluate top. Systematically explore pattern space.
---

# Pattern Exploration Strategy for C2 Optimization

## Overview
Goal: Beat 1.03492 by discovering NEW step function structures.
Small parameter tweaks will not work - we need STRUCTURAL diversity.

## Phase 1: Generate Pattern Library

1. Call generate_pattern_variants with variety="diverse"
   - Generates 50-100 patterns across all major pattern classes
   - Patterns vary in: number of levels, peak shapes, symmetry, interval count

2. Review the output patterns
   - Note: peak positions, heights, widths
   - Identify structurally distinct patterns

## Phase 2: Probe-Based Ranking

3. Extract top patterns by visual inspection or diversity criteria
   - Pick patterns that look structurally different
   - Do not pick too many similar patterns

4. Probe the candidates:
   - For each candidate, copy its code structure to EVOLVE-BLOCK
   - Call probe_solution
   - Record probe scores

5. Rank and filter:
   - Sort by probe score (descending)
   - Keep top 5-10 for evaluation
   - If scores are close, still keep them - small differences matter

## Phase 3: Full Evaluation

6. Evaluate top patterns:
   - Replace each top pattern sequentially in EVOLVE-BLOCK
   - Call evaluate_solution
   - Track which pattern gives the best combined_score

7. Analyze results:
   - If best > 1.03492: record winning pattern structure
   - If best <= 1.03492: go back to Phase 1 with different variety

## Phase 4: Iteration

8. Build on winners:
   - If you found a pattern > 1.03492, regenerate with focused variety
   - Probe and evaluate as before

9. Change strategy if stuck:
   - After 5 iterations with no improvement, try completely different classes

## Budget Management

- 30 evals total: 10 probes + 3 evals per iteration
- 6-8 iterations should use most of the budget
- Do not spend 5 evals on one pattern - probe first!
