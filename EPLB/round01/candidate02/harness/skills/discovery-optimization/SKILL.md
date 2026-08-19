---
name: discovery-optimization
description: "Iteratively optimize a program's EVOLVE-BLOCK to maximize an automatic evaluator score,\nunder a fixed evaluation budget. Use for construction, algorithm-speed, and heuristic discovery tasks\nscored by combined_score (higher is better) through the edit_solution / evaluate_solution / finish tools."
---

# Expert Parallelism Load Balancer Optimization

Key insight: This task rewards BOTH better load balancing AND faster execution.
The evaluator uses a combined_score metric. The seed program has a hierarchical
rebalancing algorithm that may have bugs or inefficiencies.

Workflow (probe-first strategy):
1. Call `probe_solution()` FIRST in EVERY iteration. This gives you a quick
   assessment of load balancing quality without consuming evaluation budget.

2. Use `probe_solution` output to decide your next edit:
   - If probe score is low: fix structural bugs first
   - If probe score is moderate: try optimization improvements
   - If probe score is high: verify with full evaluation

3. Form ONE concrete hypothesis per iteration:
   - Fix a structural bug (missing return, etc.)
   - Improve load balancing logic
   - Reduce execution time by simplifying loops
   - Add expert replication logic

4. Apply with `edit_solution` using a TARGETED SEARCH/REPLACE diff.

5. Call `probe_solution` again to verify improvement.
   If it got worse, revert and try a different approach.

6. When you have a clear improvement, call `evaluate_solution` to confirm.

7. Budget management:
   - Use probes freely
   - Use evaluations sparingly - ~20 total budget
   - Never evaluate the same code twice

8. If validity fails, read the error message carefully and fix that cause.

9. When the budget is exhausted or you cannot improve, call `finish`.

Remember: The probe tool is YOUR FRIEND. Use it in EVERY iteration to filter
candidates before spending precious evaluation budget.
