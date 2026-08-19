---
name: discovery-optimization
description: "Construct step functions with specific structures (bipartite, multi-modal, sparse) that satisfy integral(h)=1.\nUse probe_solution to screen many variants before full evaluation. Focus on reducing peak overlaps."
---

# Step Function Construction Strategy

## Core Principle
The optimal step function h likely has few intervals with specific spacing. Build structured candidates, not random ones.

## Construction Types

### 1. Bipartite Functions
- Single threshold: h(x) = 1 for x < t, 0 for x >= t (scaled)
- For domain [0,2]: h(x) = 1 for x < t * 2, 0 otherwise, where t chosen so integral = 1
- Bipartite functions have simple correlation structure

### 2. Multi-Modal Functions
- Two peaks: h has two narrow intervals where h ≈ 1, separated by region where h = 0
- Peaks at positions p1, p2 with widths w1, w2: total width = w1 + w2 = 1 (for integral = 1)
- Adjust spacing to minimize overlap at problematic k values

### 3. Sparse Functions
- Non-zero on very small intervals
- Example: three narrow peaks at 0.33, 1.0, 1.67 with width 0.1 each

## Constraint Satisfaction
- integral(h) = 1 means sum of (height * width) over all intervals = 1
- If heights are all 1, sum of widths must equal 1
- Domain is [0,2], so available "space" for width-1 regions is generous

## Evaluation Strategy
1. Construct 3-5 different structural variants
2. Use probe_solution to quickly score each
3. Evaluate top 1-2 candidates fully
4. If no improvement, try different structural templates

## Key Insight
Simple structures (2-4 intervals) may outperform complex random ones because:
- Easier to analytically compute correlations
- Fewer degrees of freedom = more predictable behavior
- The problem may have an analytical optimum with simple structure
