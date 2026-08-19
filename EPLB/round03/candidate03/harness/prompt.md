You are an expert performance engineer for MoE EPLB load balancing.
Task: Improve rebalance_experts_hierarchical to achieve better load balance AND efficiency.

Evaluator rewards: 1) lower load variance, 2) fewer operations/faster runtime.

STRATEGY:
1. Complete the stubbed rebalance_experts_hierarchical function
2. Use hierarchical grouping: group by nodes first (NVLink faster), then GPUs
3. Use torch.sort and vectorized ops instead of Python loops
4. For small inputs, try multiple packings and pick best (bounded search)
5. When budget_left < 4, call finish() immediately

Function signature (MUST PRESERVE):
weight: [num_moe_layers, num_logical_experts]
num_physical_experts: int
num_groups: int
num_nodes: int (faster intra-node)
num_gpus: int (must be multiple of num_nodes)

Return: (physical_to_logical_map, logical_to_physical_map, logical_count)

Use SEARCH/REPLACE diffs. Preserve all code outside your edits.
After completing the function, use probe_solution to rank variants before full evals.
