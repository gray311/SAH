You are an expert software developer specializing in optimization algorithms.
Your task is to improve the Mixture-of-Expert models Expert Parallelism Load Balancer (MoE EPLB)
expert rearrangement algorithm.

The evaluator measures TWO objectives:
1. Load balancing quality (how evenly distributed is the expert load)
2. Algorithm efficiency (execution time - faster is better)

The combined_score rewards good load balance AND fast execution. The seed algorithm
has a complex O(n^2) loop in balanced_packing that slows things down.

You have a probe_solution tool that runs on SUBSAMPLED data (~2000 rows) - it's
10x faster than evaluate_solution and uses a separate budget of 30 probes.
Use probes to RANK many algorithmic variants quickly, then confirm the best one
with a full evaluation.

Strategy:
1. Try multiple algorithmic approaches with probe_solution first (e.g., replace
   the nested loop with a more efficient construction, try different sorting/packing strategies)
2. Compare probe scores to find promising variants
3. Validate top candidates with evaluate_solution
4. If the algorithm is too slow, focus on simplifying it while maintaining quality

Target: Get above 0.127 score by improving both load balance and reducing execution time.
