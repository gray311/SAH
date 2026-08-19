---
name: discovery-optimization
description: "Internal variant enumeration for step-function optimization. Generate 40-50 structural variants, probe-rank them, evaluate only the best few. Focus on multi-peak, asymmetric, and height-diverse configurations."
---

# C2 Maximizer: Internal Variant Enumeration Protocol

## Core Principle

The seed provides 12 step patterns as a STARTING POINT. The harness must generate MANY variants internally (40-50) by varying heights, boundaries, and peak configurations. Only the top few (by probe) should receive full evaluation. This maximizes the chance of discovering a high-scoring variant.

## Phase 1: Broad Enumeration (iterations 1-12)

### Step 1: Generate Variants

Call enumerate_step_variants with these strategies:

**Height Variation:**
- For each of the 12 seed patterns, try heights: 0.80, 1.00, 1.20, 1.40, 1.60, 1.80, 2.00
- This gives 12 x 7 = 84 height variations

**Boundary Shifting:**
- For each pattern, shift all interval boundaries by -10%, 0%, +10% of domain
- This gives 84 x 3 = 252 boundary-shifted variants

**Hybrid Patterns:**
- Take left 50% of pattern 0 and right 50% of pattern 11
- Take left 30% of pattern 3 and right 70% of pattern 9
- Create 10 hybrid patterns x 3 height options = 30 hybrids

**Total: ~282 variants. Select TOP 40 for probing.**

### Step 2: Probe-Rank and Evaluate

- Call probe_solution on each of the 40 variants
- Rank by probe score
- Call evaluate_solution on TOP 2
- If EITHER beats current best: proceed to Phase 2. If not: continue enumeration in next iteration.

## Phase 2: Divergent Search (iterations 13-20)

### New Variant Types

**Multi-Peak Configurations:**
- Split single-peak patterns into 2, 3, or 4 peaks
- Pattern 0 (single peak) -> split into 2 peaks: heights 1.2, 1.4
- Pattern 11 (already multi-peak) -> try 3 and 4 peaks

**Asymmetric Distributions:**
- Left-skewed: tall on left, short on right
- Right-skewed: short on left, tall on right
- Try 3 variations of each

**Gaussian-Like Steps:**
- Peak at center (50%), taper to sides: 2.0, 1.5, 1.0, 0.8, 0.6
- Peak at 40%: 1.8, 2.2, 1.5, 1.0, 0.7

Generate ~50 new variants, probe all, evaluate top 3.

## Phase 3: Radical Divergence (iterations 21-25)

### Extreme Variations

**5-Peak Configurations:**
- Distribute 5 peaks across the domain with varied heights
- Pattern: 1.0, 1.8, 1.4, 2.0, 1.2

**Wide Base, Narrow Peak:**
- Broad base height 1.0 with narrow central peak 2.5
- Narrow base with broad shoulder

**Step-Gaussian Hybrid:**
- Step-like on one side, Gaussian decay on other

Generate 30 radical variants, probe top 6, evaluate best. Submit if improvement.

## Key Rules

- GENERATE 40+ VARIANTS internally per iteration
- PROBE all 40+ to rank before evaluating
- EVALUATE only TOP 2-3 by probe score
- VARY HEIGHTS across a wide range 0.80-2.00
- EXPLORE MULTI-PEAK configurations aggressively
- USE SYMMETRY-BREAKING: left-skewed vs right-skewed distributions
