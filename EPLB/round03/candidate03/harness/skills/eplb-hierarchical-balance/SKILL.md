---
name: eplb-hierarchical-balance
description: Complete MoE EPLB rebalancing with hierarchical grouping and vectorized ops. Group by nodes first (NVLink), then GPUs. Use torch.sort for speed.
---

# MoE EPLB Hierarchical Balancing Playbook

## Objective
Complete rebalance_experts_hierarchical to:
- Balance expert loads across physical replicas
- Be efficient (use torch ops, avoid Python loops)

## Function Signature
def rebalance_experts_hierarchical(
    weight: torch.Tensor,  # [num_moe_layers, num_logical_experts]
    num_physical_experts: int,
    num_groups: int,
    num_nodes: int,  # faster intra-node
    num_gpus: int
) -> tuple[physical_to_logical_map, logical_to_physical_map, logical_count]

## Implementation Steps

1. **Hierarchical Grouping**:
   - Divide experts by num_nodes: experts_per_node = num_logical_experts // num_nodes
   - For each node, balance locally
   - Then balance across nodes using num_gpus

2. **Efficient Packing** (based on seed's balanced_packing):
   - Sort weights per layer: sorted_idx = weight[i].sort(descending=True).indices
   - Pre-allocate pack_index and rank tensors
   - Use torch.argmin for tie-breaking (faster than Python min)
   - Avoid Python for-loops; use tensor indexing

3. **Replication**:
   - Compute weight/logcnt ratio
   - Use argmax to find replication targets
   - Vectorize updates

4. **Vectorized Patterns**:
   
   Bad: for i in range(num_layers): ...
   Good: all_sorted = torch.stack([weight[i].sort(...).indices for i in range(num_layers)])
   
   Bad: best = min(range(k), key=lambda x: weights[x])
   Good: best = torch.argmin(torch.tensor(weights))

5. **Bounded Search** (optional):
   - For small inputs (< 32 experts), try k packings (k=3)
   - Pick lowest variance
   - Fast and improves quality

## Example Skeleton

```python
def rebalance_experts_hierarchical(weight, num_physical_experts, num_groups, num_nodes, num_gpus):
    num_layers, num_logical = weight.shape
    
    # Hierarchical: group by node
    experts_per_node = num_logical // num_nodes
    node_groups = []
    for n in range(num_nodes):
        start = n * experts_per_node
        end = min((n+1) * experts_per_node, num_logical)
        node_groups.append(weight[:, start:end])
    
    # Balance within each node...
    # Then across nodes...
    
    return physical_to_logical_map, logical_to_physical_map, logical_count
```

## Tips
- Use torch.sort, torch.argmin, torch.stack for vectorization
- Pre-allocate all tensors
- Complete ALL parameters
- Use diagnose_load after completing to check balance
- Use probe_solution before full evals to rank variants
