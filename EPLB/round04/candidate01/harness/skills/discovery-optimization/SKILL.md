---
name: discovery-optimization
description: "Optimize MoE EPLB algorithm by vectorizing hot loops in balanced_packing(), using torch.scatter/gather for assignment, and pre-allocating arrays. Focus on execution time reduction while maintaining load balance."
---

# Vectorization-First Strategy for MoE EPLB

## Core Insight
The seed's balanced_packing() has O(n^2) Python loop overhead. Vectorization with torch operations can eliminate this entirely.

## Step 1: Analyze Hotspots
The inner loop over group in indices with for p in valid: ... is the bottleneck.
This is where vectorization wins.

## Step 2: Rewrite balanced_packing() to Vectorize
- Pre-allocate pack_index and rank_in_pack as full tensors
- Use torch.sort() with descending=True on each layer
- Replace Python min() with tensor argmin across packs
- Use scatter/gather or index arithmetic for assignment
- Avoid list comprehensions entirely

## Step 3: Iterate Strategically
- Generate variants that change the vectorization strategy
- NOT: tweak a loop limit or parameter
- BUT: try different assignment schemes (simple rank vs weight-aware)

## Step 4: Use Probe to Rank
- Probe 3-5 variants per turn
- Evaluate top 2 only

## Step 5: When Budget Runs Low
- Probe all remaining
- Evaluate best
- Finish immediately

## Entry Function
rebalance_experts_hierarchical - modify internal logic, keep signature.

## Preserve Constraints
- Exact function signatures
- torch device handling
- Return types (pack_index, rank_in_pack)
