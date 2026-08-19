---
name: c2-step-function-focus
description: Playbook for step function improvements and discretization refinements for C2 optimization.
---

# C2 Step Function Optimization Playbook

## Objective
Maximize C2 > 1.026 by improving step function representations.

## Why Step Functions?
Literature shows step functions achieve C2 = 0.8963. The seed uses 1-level steps; we can improve with:
- Multi-level steps (2-level, 3-level)
- Asymmetric configurations
- Finer discretization

## Core Strategy: Generate → Edit → Probe → Eval

1. Call generate_variants → Get 3-5 mutation suggestions
2. Pick 1-2 most promising (prefer step function improvements)
3. Use edit_solution to apply changes
4. Probe 3-5 times to rank variants
5. Evaluate only TOP 2
6. Switch strategy after 2 failed evals

## Priority Mutations

### 1. Finer Discretization (Highest Priority)
- num_intervals: 400 → 800 → 1000 → 1500
- learning_rate: 0.25 → 0.15 (slower, stable optimization)
- num_steps: 30000 → 50000 (more iterations needed)

### 2. Multi-Level Step Functions
- 2-level: high + low plateau (asymmetric)
- 3-level: three height levels
- Try different plateau widths and positions

### 3. Multi-Modal Functions
- 2-3 separated peaks
- Reduce ||f★f||_∞ by separating high-value regions

## Critical Rules

- ALWAYS call generate_variants before editing
- Probe 3-5 times per edit (never evaluate before probing)
- Evaluate only TOP 2 candidates (max 4 evals/strategy)
- Switch strategy after 2 failed evals
