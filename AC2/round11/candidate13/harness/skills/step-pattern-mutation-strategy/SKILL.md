---
name: step-pattern-mutation-strategy
description: Systematic code mutation for C2 optimization. Generate complete _create_step_initializer methods with 10-15 diverse patterns. Focus on asymmetric, multi-peak, irregular spacing architectures.
---

# Step Pattern Mutation Protocol

## Overview

Do not tweak parameters - generate COMPLETE new _create_step_initializer methods with 10-15 distinct patterns.

## What Makes a Good Pattern

- **3-6 levels** with heights in [0.5, 2.8]
- **Asymmetric heights**: avoid uniform sequences like [1.0, 1.5, 2.0]
- **Irregular intervals**: use percentages like 0.06, 0.20, 0.45, 0.70, 0.90
- **Peak asymmetry**: central peak much taller than side peaks

## Mutation Heuristics

1. **If stuck at baseline**: Try extreme asymmetry (0.5, 1.2, 2.8, 0.9, 0.5)
2. **If previous worked**: Generate 2-3 variants with similar structure
3. **If all failed**: Switch to completely different architecture class
4. **Force diversity** when no improvement in last 3 evals

## Code Template

def _create_step_initializer(self, n, pattern_idx):
    f = jnp.zeros(n)
    if pattern_idx == 0:
        f = f.at[int(0.08*n):int(0.18*n)].set(0.8)
        f = f.at[int(0.18*n):int(0.32*n)].set(1.3)
        f = f.at[int(0.32*n):int(0.52*n)].set(2.2)
        f = f.at[int(0.52*n):int(0.72*n)].set(1.4)
        f = f.at[int(0.72*n):int(0.88*n)].set(0.9)

## Common Failures

- Missing some pattern indices (must cover 0 to max)
- Heights outside [0.3, 3.0] range
- Using int(0.15*n) without float precision
- Not returning f at the end
