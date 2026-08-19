---
name: hyperparameter-search-playbook
description: Systematic hyperparameter search over principled step function constructions. Vary intervals, learning rate, penalty, steps. Use probe to rank before full eval.
---

# Hyperparameter Search Playbook for Erdős Minimum Overlap

## Overview
The seed program (800 intervals, lr=0.0053, penalty=1370, 59000 steps) achieves C5≈0.3809.
To beat this, we need both (1) new construction patterns AND (2) aggressive parameter search.

## Strategy: One-at-a-Time Search

### Phase 1: Baseline with New Constructions

Start with 2-3 new construction patterns, keeping seed hyperparameters:
- bimodal (sigma=0.15, alpha=4.0)
- periodic (duty=0.4, high=5.0, low=-5.0)
- golomb (amp=8.0)

For EACH:
1. Edit to implement the construction
2. Call probe_solution to get quick score
3. If probe score < 0.382, discard and try next construction

### Phase 2: Hyperparameter Grid Search

For constructions that beat baseline:

Vary these parameters systematically:
- num_intervals: 400, 800, 1600
- base_learning_rate: 0.001, 0.005, 0.01, 0.05
- penalty_strength: 1000, 5000, 10000
- num_steps: 30000, 60000, 100000

Test combinations with probe first, full eval only on best 3.

### Phase 3: Local Search

If best score still < 1.0:
- Take best parameters, perturb by 20 percent
- Test 5-10 perturbations with probes
- Evaluate top 2

### Key Principles

- ONE construction per edit, never multiple
- Use probe_solution extensively (30 budget)
- Keep parameter changes systematic, not random
- Track best result across all iterations
- Stop when combined_score > 1.0 or budget exhausted
