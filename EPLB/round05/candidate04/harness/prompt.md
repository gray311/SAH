You are an expert performance engineer specializing in MoE EPLB load balancing.

TASK: Replace the O(n2) balanced_packing() Python loop with O(n log n) vectorized torch code.

THE CRITICAL TRANSFORMATION:
The seed balanced_packing() function has a nested Python loop that runs O(num_groups * num_packs).
You MUST replace it with vectorized torch operations that run O(num_groups * log(num_groups)).

ALGORITHM (FOUR STEPS):
Step 1: For each layer, sort the groups by weight descending using torch.argsort
        sorted_idx = weight[i].float().sort(-1, descending=True).indices
        
Step 2: Compute pack index using integer division (broadcasting)
        pack_index[i] = sorted_idx // groups_per_pack
        
Step 3: Compute rank within pack using modulo (broadcasting)
        rank_in_pack[i] = sorted_idx % groups_per_pack
        
Step 4: Return pack_index and rank_in_pack tensors

DO NOT:
- Use list comprehensions [p for p in ...]
- Use min() with lambda
- Use append() in loops
- Iterate over groups with a Python for loop
- Import numpy (use torch only)

EVALUATION:
- Higher combined_score = better load balancing + faster execution
- Seed score: 0.127163. You MUST exceed this.
- Use probe_solution to test your edit before evaluate_solution

BUDGET: ~20 evaluations total. Generate ONE correct edit, probe it, evaluate it.
