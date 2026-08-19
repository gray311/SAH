---
name: discovery-optimization
description: "Generate diverse patterns via search_patterns, then MUTATE the best pattern with mutate_best_pattern\nto create refined variants. Screen all with probe_solution, evaluate top candidates only."
---

# Erdos C5 Optimization - Pattern Refinement Strategy

## Phase 1: Generate Diverse Patterns

1. CALL search_patterns(temperature=0.5)
   - Returns 5 candidates with precomputed c5_bound via FFT
   - Each satisfies integral=1, h in [0,1]
   - Patterns: Golomb (4 marks), Bipartite, Triangular, Multi-peak, Laplace

2. IDENTIFY best candidate (lowest c5_bound)
   - Example: If bipartite has c5_bound=0.378 and others are 0.382+, select bipartite

## Phase 2: Mutate Best Pattern

3. CALL mutate_best_pattern with the best candidate

   This tool creates 3 refined variants by:
   - Adjusting peak widths (±10%)
   - Shifting peak centers (±0.1 units)
   - Modifying peak amplitudes (±0.2)
   
   All variants satisfy integral(h)=1 and h in [0,1].
   Each variant has precomputed c5_bound via FFT (instant).

4. EXAMINE all 3 mutated variants
   - Find the one with lowest c5_bound
   - Keep only those with c5_bound < 0.375

## Phase 3: Screen and Evaluate

5. CALL probe_solution on each mutated variant with c5_bound < 0.375
   - Probe is cheap (separate budget, ~10s per call)
   - Keeps evaluation budget for the best candidates

6. CALL evaluate_solution on TOP 1-2 candidates with lowest probe scores
   - Full optimization takes ~59000 steps
   - Only evaluate if c5_bound < 0.375 (combined_score > 1.01)

## Phase 4: If No Improvement

7. If all evaluations yield combined_score <= 1.0:
   - Call search_patterns(temperature=0.8) for different patterns
   - Repeat Phase 2-3

## Phase 5: Hyperparameter Tuning (LAST RESORT)

Only after exhausting pattern-based search, tune:
- num_intervals: 400, 800, 1600, 3200
- base_learning_rate: 0.001, 0.005, 0.01
- penalty_strength: 40, 80, 120

## Critical Rules

- ALWAYS use search_patterns FIRST
- ALWAYS call mutate_best_pattern on the best pattern (don't skip to tuning)
- NEVER evaluate unless c5_bound < 0.375
- Use probe_solution to screen before full evaluation
- Stop when combined_score > 1.0
