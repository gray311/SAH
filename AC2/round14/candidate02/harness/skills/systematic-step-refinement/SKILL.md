---
name: systematic-step-refinement
description: Systematic single-parameter mutation protocol for step-function C₂ optimization. Focus on ONE parameter change per iteration to understand causality.
---

# Systematic Step-Function Refinement Protocol

## Core Principle
Step functions work through careful parameter tuning. To beat the record, make SMALL, TARGETED changes to ONE parameter at a time.

## Mutation Protocol
### Cycle 1: Height Exploration
1. Use step_pattern_analyzer to identify current heights
2. Pick ONE height level
3. Perturb by ±0.03 to ±0.08
4. Call probe_solution to check score
5. If improvement: continue in same direction; else try ±0.05

### Cycle 2: Width Exploration
1. Use step_pattern_analyzer to identify current widths
2. Pick ONE interval
3. Change boundary by ±3% to ±8%
4. Call probe_solution
5. Prefer expanding the "core" (tallest) interval

### Cycle 3: Position Exploration
1. Pick ONE boundary
2. Shift by ±1-2% of domain
3. Call probe_solution
4. Test both left and right shifts

## Ranking & Evaluation
1. Generate 3-5 mutations (different parameters)
2. Probe ALL of them (use your 30 probes!)
3. Evaluate top 2 by probe score
4. If BOTH fail: reset and try next cycle
5. If ONE succeeds: refine that parameter further

## When to Explore New Families
Only after exhausting 3+ mutation cycles without improvement:
- Try Gaussian mixtures, splines, etc.
- But expect them to UNDERPERFORM step functions
- Return to step refinement if they fail

Key: Systematic, single-parameter mutations beat random exploration.
