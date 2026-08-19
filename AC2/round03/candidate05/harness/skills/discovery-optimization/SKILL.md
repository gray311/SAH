---
name: discovery-optimization
description: "Maximize C2 for second autocorrelation. Seed optimized piecewise-linear. SWITCH to multi-level steps or Gaussian mixtures using templates. Probe 5+ variants before evaluating. Max 2 evals per family."
---

# C2 Family Switch Protocol

## Objective
Beat 0.8963 record. Current best: ~0.914 with piecewise-linear.

## Critical Insight
You optimized piecewise-linear. DO NOT tune it further. SWITCH to new function families.

## Protocol

### Step 1: Choose Family
Use one of these templates:

A. Multi-level steps:
```
def _create_initializer(self, key, pattern_idx):
    n = self.hypers.num_intervals
    f = jnp.zeros(n)
    if pattern_idx == 0:
        f = f.at[int(0.15*n):int(0.35*n)].set(1.0)
        f = f.at[int(0.35*n):int(0.55*n)].set(2.0)
        f = f.at[int(0.55*n):int(0.75*n)].set(1.5)
        f = f.at[int(0.75*n):int(0.95*n)].set(0.8)
    return f
```

B. Gaussian mixtures:
```
def _create_initializer(self, key, pattern_idx):
    n = self.hypers.num_intervals
    K = 3 if pattern_idx < 3 else 5
    means = jnp.linspace(0.1, 0.9, K)
    sigmas = jnp.ones(K) * (0.05 + pattern_idx * 0.02)
    f = jnp.zeros(n)
    for k in range(K):
        gaussian = jnp.exp(-0.5 * ((jnp.arange(n) - means[k] * n) / sigmas[k])**2)
        f = f + 0.5 * gaussian
    return f
```

### Step 2: Probe 5 Variants
Create variants by changing parameters. Call probe_solution on each.

### Step 3: Evaluate Top 2
Pick 2 highest-probe variants. Call evaluate_solution on each.

### Step 4: Decision
Improvement? Deepen. No improvement? SWITCH to different family.

## Rules
- 5+ probes per family
- Max 2 evals per family
- Switch families immediately on stagnation

## Tools
| Tool | When |
|------|------|
| edit_solution | Replace _create_initializer with template |
| probe_solution | Rank variants |
| evaluate_solution | Confirm top 2 only |
| finish | When exhausted |

## Success Path
1. Replace _create_initializer with steps template
2. Probe 5 variants
3. Evaluate top 2
4. If no improvement: switch to Gaussian mixtures
5. Repeat
