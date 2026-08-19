---
name: load-balancing-playbook
description: Playbook for optimizing MoE EPLB load balancing algorithm. Focus on reducing load variance and execution time.
---

# Load Balancing Optimization Playbook

## Step 1: Analyze Current State
Use probe_strategy() to check load distribution. Identify if:
- Load is highly skewed (std >> mean)
- Some layers have extreme variance
- Total computation is O(n²) or worse

## Step 2: Choose Technique Based on Analysis
- If skewed: Try FIRST FIT DECREASING (sort descending, place in lightest available pack)
- If balanced but slow: Optimize to vectorized torch operations, avoid Python loops
- If many ties: Break ties by depth or weight, not randomly

## Step 3: Implement with Vectorization
REWRITE balanced_packing() to:
- Pre-allocate all output arrays
- Use torch operations: sort, scatter, gather
- Avoid list comprehensions [p for p in ...]
- Use min() with key lambda only when necessary

Example transformation:
OLD: for group in indices: for p in valid: ...
NEW: idx = np.argsort(-weight[i])
ranks = np.zeros(num_groups, dtype=int)
for i in range(groups_per_pack):
    for j in range(i * groups_per_pack, min((i+1) * groups_per_pack, num_groups)):
        ...

## Step 4: Test and Refine
- Use probe_solution with subsample to quickly rank
- Run evaluate_solution on best 1-2 variants
- If score doesn't improve, try next technique
- NEVER retry the same technique with different parameters

## Step 5: Finish Strategy
When budget_left < 5: 
1. Probe all remaining variants
2. Submit best via evaluate_solution
3. Call finish immediately after result
