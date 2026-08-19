---
name: discovery-optimization
description: "Search-based candidate generation: edit seed to vary random seeds and restarts, then screen with probe_solution."
---

# Search-Based Candidate Generation for Erdos Optimization

## Why the Seed Optimizer

The seed optimizer runs 59000 training steps per candidate. It supports multiple restarts (num_restarts=3) with different seeds. We need to leverage this by:

1. Creating 3-4 different initial configurations by changing num_restarts and seed_start
2. Using probe_solution to quickly filter (cheap)
3. Only evaluating promising candidates with evaluate_solution

## Workflow

### Step 1: Generate Candidates via Edit

Edit the seed to vary num_restarts and seed_start:
- Baseline: num_restarts=3, seed_start=0 (already good)
- Alternative 1: num_restarts=1, seed_start=1 (single restart, different seed)
- Alternative 2: num_restarts=1, seed_start=2
- Alternative 3: num_restarts=1, seed_start=3
- Alternative 4: num_restarts=2, seed_start=1 (fewer restarts, explore seeds)

Each edit creates a new candidate that the optimizer will train.

### Step 2: Screen with probe_solution

For each candidate, first call probe_solution (uses 500 intervals, fast):
- Returns approximate c5_bound and integral estimate
- Takes ~10 seconds vs minutes for full eval
- Does NOT consume evaluation budget

Filter: Keep only if probe c5_bound < 0.37 AND integral close to 1.0

### Step 3: Full Evaluation

For candidates passing probe screening, call evaluate_solution:
- Full 800-interval evaluation
- Uses the real evaluation budget (30 total)
- Returns accurate combined_score = 0.38092303510845016 / c5_bound
- combined_score > 1.0 means new record!

### Step 4: Iterate or Finish

- If any evaluate_solution returns combined_score > 1.0, call finish()
- If no improvement after 3-4 iterations, EDIT to try:
  - Golomb ruler initialization (edit _get_best_initialization pattern)
  - Different random seeds
  - Fewer intervals (e.g., num_intervals=200) for faster exploration

## Example Tool Calls Sequence

1. EDIT (num_restarts=1, seed_start=1)
2. probe_solution -> c5=0.365, integral=0.998 -> PASS
3. evaluate_solution -> combined_score=1.05 -> RECORD!
4. finish("Found c5=0.366 with num_restarts=1, seed_start=1")

## Why This Works

- Uses seed optimizer's built-in diversity (multi-restart)
- probe_solution is cheap for screening (10s vs 5-10 min per eval)
- evaluate_solution budget (30) is used only on promising candidates
- No reliance on broken analytical tools

## Golomb Ruler Initialization (Alternative)

If standard random seeds fail, EDIT to use explicit Golomb ruler marks:
Edit _get_best_initialization to use pattern==12 with marks [0.0, 0.4, 0.8, 1.2, 1.6]
Golomb rulers minimize max overlap by design.
