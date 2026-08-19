---
name: pattern-exploration-protocol
description: Step-function pattern diversification using JAX array mutations. Generate diverse configurations, not just parameter tweaks.
---

# Pattern Exploration Protocol for C2 Maximization

## Core Principle
The seed step patterns are fixed. You must GENERATE NEW pattern families, not just tweak parameters.

## Phase 1: Pattern Diversification (iterations 1-12)

1. Call generate_pattern_variants to get 3-4 diverse patterns:
   - Wider peak (expand width to 55% of domain)
   - Two-peak config (split domain into two regions, each ~40% with peak)
   - Asymmetric (left peak taller than right by 15-25%)
   - Concentrated (narrow high peak in 40% of domain, height 2.0-2.5)

2. For EACH pattern, generate CONCRETE JAX edits:
   - f = f.at[start:end].set(value)
   - Use integer indices: start = int(0.28 * n), end = int(0.72 * n)
   - Heights: 1.2-2.5, avoiding overflow

3. Call probe_solution on ALL variants (spend 10-12 probes)

4. Evaluate top probe score

## Phase 2: Structural Refinement (iterations 13-22)

1. Identify winning pattern features (peak count, height ratio, width)
2. Generate 2 variants:
   - Add one more peak (if 2-peak → 3-peak)
   - Adjust height ratios: tallest / shortest = 1.3 to 1.8
3. Probe both, evaluate best

## Phase 3: Aggressive Exploration (iterations 23-29)

1. If stuck, generate "high-diversity" patterns:
   - 4-peak configuration
   - Concentrated: 90% energy in 20% domain (height 2.5-3.0)
   - Gaussian-like: smooth transitions with softplus
2. Probe 3, evaluate best
3. Submit if c2 > 0.8962799441554086

## Key Rules
- GENERATE DIVERSE PATTERNS, not parameter tweaks
- Use CONCRETE JAX syntax: f.at[start:end].set(value)
- Probe 8-10 variants before any full eval
- Multi-peak patterns often outperform single-peak
