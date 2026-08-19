---
name: combinatorial-search-playbook
description: Systematic exploration of multi-level step function parameter space. Use parameter variations rather than random edits. Methodical search beats random mutations.
---

# Combinatorial Search for Multi-Level Step Functions

## Core Principle: Systematic Parameter Exploration

The C₂ optimization problem has a combinatorial structure:
- Multiple levels (2-6)
- Each level has height, width, position

Random mutations rarely find the optimum. Instead, systematically explore:

### 1. Parameter Space Grid

Think of parameters as a grid to explore:

- num_intervals: [300, 400, 500, 600]
- learning_rate: [0.15, 0.20, 0.25, 0.30, 0.35]
- reinit_fraction: [0.10, 0.15, 0.20, 0.25, 0.30]
- Central height: [0.7, 1.0, 1.3, 1.6, 2.0]

Don't random-walk through this space. Use structured sweeps.

### 2. Search Protocol

**Iteration 1: Baseline Sweep**
- Start with seed's parameters
- Generate 5 variations by tweaking 1-2 parameters at a time
- Probe all 5
- Evaluate the best

**Iteration 2: Expand on Success**
- If baseline+δ worked, try baseline+2δ
- If baseline worked better, try neighbors
- Keep exploring in the promising direction

**Iteration 3+: Systematic Coverage**
- If no single-parameter sweeps worked, try 2-parameter combinations
- Try different initial heights (lower vs higher)
- Try different symmetries (symmetric vs asymmetric)

### 3. Decision Tree

If probe scores show:
- Clear direction: Exploit (go further in that direction)
- Mixed results: Explore (try orthogonal parameter changes)
- All bad: Restart with completely different parameter regime

### 4. Budget Allocation

With 20 evals total:
- Early iterations (5-7): Use 2 evals each, heavy probing
- Mid iterations (4-5): Use 2 evals each
- Late iterations (3-4): Use 1 eval each, confirm top candidates

Total: ~16-18 evals leaves buffer for retry

### 5. Common Patterns to Try

If stuck, these patterns often work:

1. **Higher central peak**: Increase central height to 2.0-2.5
2. **Wider support**: Expand the central region to 60-70%
3. **Multi-level complexity**: Add 4-5 levels with varying heights
4. **Asymmetric profile**: Make one side wider than the other
5. **Sharper transition**: Reduce interval count but increase heights

## Checklist

- [ ] Using generate_pattern_variation for systematic exploration
- [ ] Probing 3-5 variants before each eval
- [ ] Only 1-2 evals per iteration
- [ ] Tracking which parameter changes helped
- [ ] Restarting strategy if 5 iterations with no progress'
