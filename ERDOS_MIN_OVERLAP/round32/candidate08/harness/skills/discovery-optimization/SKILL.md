---
name: discovery-optimization
description: "Systematic hyperparameter search for Erdos C5.\nUse hyperparameter_tuner for suggestions, focus on penalty_strength and num_intervals.\nCall probe_solution before evaluate_solution."
---

# Erdos C5 Hyperparameter Search

The seed program is an optimizer class. Key is tuning hyperparameters,
not analyzing h array (computed during optimization, not static).

## Key Parameters

- penalty_strength (default 61): Enforce integral(h)=1. Try 80-150.
  Too low: constraint violation. Too high: poor optima.

- num_intervals (default 800): Discretization. Try 400-1600.

- base_learning_rate (default 0.004): Try 0.001-0.01.

- num_steps (default 120000): More = better optima. Try 40k-200k.

- num_restarts (default 3): Multi-restart count. Try 1-10.

## Strategy

Phase 1: Run baseline with defaults.

Phase 2: Vary ONE parameter at a time:
  - penalty_strength: 80, 100, 120, 140, 150
  - num_intervals: 400, 600, 800, 1000, 1200, 1400, 1600

Phase 3: For each variation, call probe_solution first.
Call evaluate_solution only if probe shows c5_bound < 0.382.

Phase 4: If single-var fails, try combinations:
  - penalty_strength=100 with num_intervals=600
  - penalty_strength=120 with num_intervals=1000

Rules:
- Use hyperparameter_tuner BEFORE editing
- Change ONE parameter at a time
- Use probe_solution to screen
- Systematic search beats random changes
