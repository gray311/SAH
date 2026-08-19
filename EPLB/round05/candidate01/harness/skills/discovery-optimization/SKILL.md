---
name: discovery-optimization
description: "Transform O(n^2) balanced_packing() to O(n log n) vectorized torch code.\nUse vectorize_balanced_packing tool for template generation."
---

# Vectorized EPLB Optimization via Scaffold

## Step 1: Get Vectorized Template

Call vectorize_balanced_packing() immediately. This tool provides a working
vectorized implementation template. DO NOT try to write vectorized code from scratch.

## Step 2: Customization

After getting the template:
1. Verify function signature matches: balanced_packing(weight: torch.Tensor, num_packs: int)
2. Check it uses: torch.argsort(-weight, dim=-1) for sorting
3. Verify pack_assignment = sorted_idx // groups_per_pack
4. Verify rank_assignment = sorted_idx % groups_per_pack
5. Ensure pack_weights computed via boolean indexing or scatter

## Step 3: Integration

Replace ENTIRE balanced_packing() function body with your vectorized version.
Preserve imports (torch) and docstring.

## Step 4: Validation

- Call probe_solution 2-3 times on variants
- If any probe > seed (0.127), call evaluate_solution
- Use the best variant

## Step 5: Budget Management

- Use probe extensively when budget_left > 5
- Evaluate top 1-2 variants with evaluate_solution
- Call finish immediately after final evaluation

## Key Transformations

- For loop: "for group in indices" → argsort + broadcasting
- List comprehension: [p for p in range(...) if ...] → boolean mask
- min() with lambda → direct indexing or scatter
- append/grow → pre-allocate tensors
