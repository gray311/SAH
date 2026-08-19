---
name: pattern-discovery-method
description: Systematic pattern search for Erdos C5 minimization. Focus on Golomb ruler and tri-modal patterns.
---

# Pattern Discovery for Erdos Problem

## Core Principle

This is a PATTERN DISCOVERY problem. The seed optimizer is well-tuned (lr=0.006, steps=59000, penalty=60). Focus on finding BETTER INITIAL PATTERNS, not tuning hyperparameters.

## Step 1: Generate Integral-Constrained Candidates

CALL generate_ready_candidates(temperature=0.5) once.

Returns 3 candidates (Golomb, Bipartite, Tri-modal) with integral(h)=1 exactly.

VERIFY integral ~ 1.0 for each. If not, discard.

## Step 2: Screen with probe_solution

For each candidate, call probe_solution to get approximate c5_bound.

FILTER:
- c5_bound < 0.375: PROMISING, move to full eval
- c5_bound < 0.385: MARGINAL, may still be worth testing
- c5_bound >= 0.385: DISCARD

## Step 3: Full Evaluation

Call evaluate_solution on candidates with c5_bound < 0.370.

Stop as soon as combined_score > 1.0.

## Step 4: If Stuck, Vary Pattern Parameters

### Golomb Ruler Variations:
- Try 4 marks: [0.0, 0.5, 1.0, 1.5] (coarser)
- Try 5 marks denser: [0.0, 0.33, 0.66, 1.33, 1.66]
- Try asymmetric: [0.0, 0.25, 0.75, 1.25, 1.75]

### Tri-Modal Variations:
- Move peaks: [0.25, 1.0, 1.75] or [0.3, 1.0, 1.7]
- Add 4th peak: [0.2, 0.7, 1.0, 1.7]

### Bipartite Variations:
- Change split: threshold at 0.4, 0.6, or 0.7

## Budget Discipline

- 30 probe_budget: screen 10-20 pattern variants
- 60 eval_budget: spend max 5-10 full evaluations
- STOP when you find improvement OR exhaust probes with no < 0.375 candidate
