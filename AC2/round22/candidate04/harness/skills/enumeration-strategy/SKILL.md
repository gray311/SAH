---
name: enumeration-strategy
description: Step-function variant generation protocol - create 40-50 internal variants by height variation, boundary shifting, hybrid patterns, and multi-peak configs. Probe-rank all before evaluating.
---

# C2 Maximizer: Internal Variant Enumeration Protocol

## Core Strategy

The seed provides 12 step patterns. The harness must generate MANY variants internally (40-50) and probe-rank them before evaluation. This maximizes discovery of high-scoring variants.

## Phase 1: Broad Enumeration

### Generate Variants

1. Height Variation: For each seed pattern, try heights 0.80, 1.00, 1.20, 1.40, 1.60, 1.80, 2.00
2. Boundary Shifting: Shift boundaries by -10%, 0%, +10% of domain
3. Hybrid Patterns: Combine left/right halves of different seeds
4. Multi-Peak: Split single peaks into 2-4 peaks

### Probe and Evaluate

1. Call enumerate_step_variants to generate 45 variants
2. Probe all 45 variants (45 probes total - budget is sufficient)
3. Rank by probe score
4. Evaluate TOP 2 variants

## Phase 2: Divergent Search

Generate 50 new variants with:
- 3-5 peak configurations
- Asymmetric left/right distributions
- Gaussian-like step functions
- Wide base with narrow peak

Probe all, evaluate top 3.

## Phase 3: Radical Divergence

Generate 30 extreme variants:
- 5+ peaks with varied heights
- Step-Gaussian hybrids
- Wide base narrow peak extremes

Probe top 6, evaluate best. Submit if improvement.

## Key Rules

- ALWAYS generate 40+ variants internally per iteration
- ALWAYS probe 40+ before evaluating
- VARY HEIGHTS across 0.80-2.00 extensively
- EXPLORE MULTI-PEAK configurations aggressively
- USE SYMMETRY-BREAKING: left vs right skewed
