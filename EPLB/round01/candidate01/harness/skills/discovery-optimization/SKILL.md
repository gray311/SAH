---
name: discovery-optimization
description: "Optimize MoE EPLB load-balancing algorithms by applying domain-specific transformations (vectorization, loop elimination, hierarchical decomposition)."
---

# MoE EPLB Algorithm Optimization Method

## Objective
Maximize the combined score by improving both load balancing and execution efficiency.
Score = f(load_balance_quality, execution_time_efficiency)

## Step 1: Structural Analysis
Before editing, call analyze_algorithm to understand:
- Number of MoE layers and logical experts
- Weight tensor shape
- Existing loop structure and computational hotspots

## Step 2: Optimization Patterns (Apply ONE per edit)

### Pattern A: Vectorize Python Loops
Replace nested Python for-loops with torch operations:
- for loops over groups/experts → torch.gather, torch.scatter, torch.sort
- for loops finding min → torch.min, torch.argmin
- Accumulators → torch.cumsum, torch.scatter_add

### Pattern B: Pre-compute Indices
Instead of computing indices inside loops, pre-compute with:
- torch.arange for pack indices
- torch.meshgrid or torch.stack for pairing operations

### Pattern C: Replace Manual Min-Finding
Current pattern: min(pack_weights.__getitem__()) is O(n) in a loop
Better: torch.argmin(pack_weights, dim=0) then use that index

### Pattern D: Use Sort-Based Assignment
For balanced packing, sort by weight (descending), then assign:
- Sort once globally
- Assign round-robin or modulo-based distribution
- Avoid per-iteration min-finding

## Step 3: Evaluation Strategy
1. Edit with ONE pattern applied
2. Evaluate and record score
3. If valid but score less than best_so_far, revert and try a DIFFERENT pattern
4. If invalid (validity=0), analyze error, fix the specific bug
5. Continue until budget exhausted

## Step 4: When to Stop
Call finish when:
- Budget exhausted
- Score plateaued despite trying 3+ different patterns
- Cannot find another valid optimization direction
