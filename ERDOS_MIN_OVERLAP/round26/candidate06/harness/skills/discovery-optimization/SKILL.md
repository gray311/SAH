---
name: discovery-optimization
description: "Analytical screening first, then structural pattern edits, then hyperparameter tuning.\nUse generate_ready_candidates to get integral-constrained baselines.\nExplore pattern 5, 12, 14 definitions with SPECIFIC mark/peak changes.\nUse probe_solution for all screening."
---

# Erdos C5 Solver - Method Guide

## Phase 1: Analytical Baselines (0 evals needed)

1. CALL generate_ready_candidates(temperature=0.5)
2. EXAMINE candidates returned:
   - Each has: h (latent), integral, c5_bound, pattern_type
   - Check: c5_bound values - typically 0.37-0.39 range
3. IF ANY candidate has c5_bound < 0.37:
   - CALL evaluate_solution on it
   - Report combined_score
4. IF ALL candidates have c5_bound >= 0.37:
   - Move to Phase 2

## Phase 2: Structural Pattern Edits (EXPAND SEARCH SPACE)

The seed has 15 initialization patterns. Focus on patterns 5, 12, 14 which use
specific mark/peak definitions. Edit these to try new configurations.

### Pattern 5 (Bipartite):
Original: x < 0.5: 4.0, x >= 0.5: -1.0
TRY:
  - x < 0.4: 4.0, x >= 0.4: -1.0
  - x < 0.6: 4.0, x >= 0.6: -1.0
  - x < 0.7: 4.0, x >= 0.7: -1.0

### Pattern 12 (Golomb ruler - 5 marks):
Original: marks = [0.0, 0.4, 0.8, 1.2, 1.6]
TRY:
  - marks = [0.0, 0.5, 1.0, 1.5, 2.0]  # equally spaced
  - marks = [0.0, 0.3, 0.9, 1.5, 2.0]  # irregular
  - marks = [0.1, 0.6, 1.1, 1.6, 2.0]  # shifted
  - marks = [0.0, 0.4, 0.7, 1.4, 1.8]  # compressed

### Pattern 14 (Tri-modal - 3 peaks):
Original: peaks = [0.4, 1.0, 1.6]
TRY:
  - peaks = [0.3, 1.0, 1.7]
  - peaks = [0.4, 0.9, 1.6]
  - peaks = [0.35, 1.05, 1.65]
  - peaks = [0.2, 1.0, 1.8]

### Pattern 13 (Bipartite variant):
Original: x < 0.6: 3.0, x >= 0.6: -3.0
TRY:
  - x < 0.5: 3.0, x >= 0.5: -3.0
  - x < 0.55: 3.0, x >= 0.55: -3.0

## Phase 3: Probing and Evaluation

1. For each pattern edit:
   - CALL edit_solution with the specific change
   - CALL probe_solution to get approximate c5_bound
   - IF c5_bound < 0.37: CALL evaluate_solution
   - IF c5_bound >= 0.37: discard, try next edit

2. Track best c5_bound seen so far.

## Phase 4: Hyperparameter Tuning (if still stuck)

Only if Phase 2 yields no improvement:
- Vary num_intervals: 400, 1600, 3200
- Vary base_learning_rate: 0.01, 0.02
- Vary penalty_strength: 40, 80
- ALWAYS use probe_solution first

## Key Rules

- NEVER change all hyperparameters at once
- ALWAYS use probe_solution before evaluate_solution
- Make SPECIFIC edits (e.g., "change 0.4 to 0.5"), not vague changes
- If no improvement after 20 iterations, RESTART with fresh pattern ideas
- Expected: c5_bound < 0.37 (combined_score > 1.027)
