---
name: step-function-search
description: Use enumerate_step_functions to directly construct step functions with integral=1. Evaluate them immediately - no training needed.
---

# Step Function Search Strategy

## Key Insight
The Erdos C5 problem is about discrete step function CONSTRUCTIONS, not gradient training.
Step functions naturally satisfy the integral=1 constraint and give exact C5 bounds.

## Workflow

1. CALL enumerate_step_functions(pattern_type="auto", num_variants=5)
   - Generates 10+ step functions with integral=1
   - Each has precomputed c5_bound via FFT (exact, no training)

2. EXAMINE candidates sorted by c5_bound:
   - Best should have c5_bound < 0.3809 (current best)
   - Look for patterns: bipartite (2 segments), trimodal (3 peaks), etc.

3. CALL evaluate_solution on TOP 3 candidates with c5_bound < 0.375
   - Step functions are READY - no training needed
   - Full evaluation gives exact C5 bound

4. If combined_score > 1.0, finish immediately!

5. If no improvement:
   - Try enumerate_step_functions with specific pattern_type: "bipartite", "trimodal", "quadrisection"
   - Then try seed optimizer as fallback

## Expected Outcome

Well-designed step functions should achieve c5_bound < 0.37, giving combined_score > 1.05.
The optimal construction is likely a symmetric or near-symmetric step function.
Save the budget - step functions require only 1 tool call + 2-3 evals max.
