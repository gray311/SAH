---
name: discovery-optimization
description: "Analytical screening via generate_ready_candidates, FFT diagnostics via analyze_fft_spectrum, then focused hyperparameter tuning only when stuck."
---

# Erdos C5 Solver - Analytical Screening Strategy

## PHASE 1: Analytical Screening (MUST DO FIRST)

1. CALL generate_ready_candidates() with temperature=0.5

2. EXAMINE the 3 returned candidates:
   - Each has precomputed c5_bound via FFT
   - Each has integral (should be ~1.0)

3. FILTER:
   - SKIP candidates with integral != 1.0 (constraint violation)
   - SKIP candidates with c5_bound >= 0.375 (too bad)
   - KEEP candidates with c5_bound < 0.37

4. CALL evaluate_solution on ALL kept candidates.
   - Full eval is expensive (59000 steps) but gives real score
   - Record best combined_score

5. If NO candidate gave combined_score > 1.0:
   - Stop immediately
   - Call finish() with summary

## PHASE 2: FFT Diagnosis (ONLY if Phase 1 failed)

1. CALL analyze_fft_spectrum() to diagnose current seed:
   - Report: peak_locations, energy_spectrum, max_overlap_index

2. If FFT shows clear structure (e.g., peaks at 0.5, 1.5), edit ONE of:
   - num_intervals: 800 -> 1600 (finer grid to capture peaks better)
   - base_learning_rate: 0.006 -> 0.01 (faster convergence)

3. CALL probe_solution on edited version (cheap check)

4. If probe c5_bound < 0.38, CALL evaluate_solution

5. If still stuck after 1 edit: STOP and call finish()

## WHY THIS WORKS

- generate_ready_candidates: O(1) analytical scores, no training needed
- analyze_fft_spectrum: Diagnoses WHY current h is bad
- Focus: Only ~3-5 full evals, not 30

## FAILURE MODES TO AVOID

- DON'T edit num_steps, penalty_strength, num_restarts (don't change optimizer behavior)
- DON'T try to "learn" better patterns (already have 15 in seed)
- DON'T call analyze_fft_spectrum before generating candidates
