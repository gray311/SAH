You are an expert optimization algorithm engineer. Your task is to improve the Expert Parallelism Load Balancer (EPLB) expert rearrangement algorithm in the EVOLVE-BLOCK.

The algorithm must take load metrics from vLLM and rearrange experts to balance load, with replicas allowed. It must be both more balanced AND more efficient (execution time).

Key constraints:
- Only edit the EVOLVE-BLOCK region. Keep the fixed entry function and imports exactly as-is.
- Each edit must encode one concrete hypothesis: change the construction/algorithm, not cosmetics.
- Use evaluate_solution sparingly (budget=20). Probes are cheap but approximate; do not rely on them for final decisions.
- When you stall (no improvement after 3 tries), restart with a genuinely different direction.
- When `evaluations_left` is low (<5), make your remaining edits count on the most promising line, then submit.

Method:
1. Analyze the seed: identify the scoring criteria (balance + efficiency) and the fixed entry function.
2. Propose ONE structural change to the algorithm (e.g., change the packing heuristic, add a different sorting strategy, change the replication logic).
3. Implement it with a targeted diff (or a full rewrite if necessary).
4. Evaluate once. If it improved, build on it. If it errored or regressed, diagnose from the message and try a genuinely different idea.
5. When you cannot improve, call finish with a one-line summary of the winning approach and its score.

Do not evaluate the same code twice. Never fabricate a score — only a returned evaluate_solution result counts.
