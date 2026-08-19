---
name: probe-first-exploration
description: Use probe_solution to screen multiple variants cheaply before full evaluation. Focus on structural code changes rather than hyperparameter tuning.
---

# Probe-First Exploration Strategy

## Core Principle
Use cheap probes to rank variants before spending expensive full evaluations.

## Workflow

1. Generate 5 structural variants (structural_variants tool).

2. Probe all 5 variants:
   - Call probe_solution for each edit
   - Record c5_bound scores
   - Typical probe: ~10 seconds, very cheap

3. Rank by probe score (lowest c5_bound = best)

4. Select top 2-3 variants for full evaluation:
   - Call evaluate_solution on each
   - Record combined_scores

5. If best new score > 1.0, we found improvement!

6. If no improvement, generate new variants and repeat.

## Budget Management

- Probes: Use 5-7 (plenty for screening)
- Full evals: Use 2-6 (only on promising variants)
- Total budget: 20 evals available

## Why Probe-First Works

- Full evals take minutes each - use sparingly
- Probes are fast - can screen many variants
- Structural changes have large effects - easy to rank with probes
- Avoid wasting evals on clearly bad variants
