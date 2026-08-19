---
name: probe-first-exploration
description: Parallel diverse generation with aggressive probe ranking. Use probes to filter before full evals.
---

# Probe-First Diverse Exploration for C₂ Maximization
## Core Principle
With only 30 full evaluations and 30 probes available, the optimal strategy is: 1. GENERATE diverse architectures 2. RANK with PROBES (cheap, separate budget) 3. EVALUATE only top candidates 4. REPEAT with new families
This avoids wasting full evals on weak proposals.
## Phase 1: Aggressive Diverse Generation
Every iteration (or when stuck): - Call generate_architectures for 5-7 proposals - Ensure diversity: check you're not repeating the same family type - If you've tried all smooth families, try sharp ones (steps, wavelets) - Vary: number of components, decay rates, symmetry, polynomial degrees
## Phase 2: Probe-First Ranking (DO NOT SKIP)
1. Call probe_solution for EACH proposal (5-7 probes per iteration) 2. Probes are YOUR PRIMARY ranking mechanism: - 10x faster than full evaluation - 30-probe budget (separate from 30 evals) - Approximate scores sufficient for ranking 3. If probe score < current best (1.03896), SKIP full evaluation 4. Select TOP 3-4 by probe score for Phase 3
## Phase 3: Strategic Full Evaluation
1. Evaluate only the 3-4 highest-probe-score proposals 2. Track which family/architecture beats the record 3. If NO winner after 3-4 evals: return to Phase 1 with FRESH families 4. If a winner is found: make 1-2 small refinements, then immediately return to Phase 1
## Phase 4: Diversity Maintenance
- Every 5 iterations: explicitly generate from underexplored families - Diversity checklist: smooth vs. sharp, symmetric vs. asymmetric, single vs. multi-peaked, decaying vs. non-decaying - If stuck for 10 iterations: call generate_architectures again with focus on completely new families
## Expected Outcome
Within 15-20 iterations, one architecture family should beat the step-function record. The key is PARALLEL EXPLORATION with PROBE-GATING to avoid evaluation budget exhaustion on dead-end families.
