---
name: minimal-edit-strategy
description: Use minimal, targeted edits with probe-based validation for Erdos optimization.
---

# Minimal Edit Strategy for Erdos Problem

## DO NOT do complex multi-change edits.

## DO make one change at a time:
- Change ONE learning rate (try 0.01, 0.001, 0.02)
- Change ONE penalty strength (try 500, 5000, 15000)
- Change ONE number of intervals (try 1600, 400, 16000)
- Add ONE construction type to initialization

## AFTER each edit:
1. Call probe_solution to check if it helps
2. If probe improves, consider full evaluation
3. If probe worsens, revert mentally and try different edit

## When stuck:
- Try a completely different construction pattern
- Reduce penalty strength to avoid over-constraining
- Increase resolution (num_intervals) to see finer patterns

## Remember:
- Probe is FREE (separate budget), use it generously
- Evaluation is expensive (30 total), use sparingly
- Small changes often beat large rewrites
