---
name: direct-generation-strategy
description: Generate step functions directly with constraint satisfaction, bypassing the broken optimizer.
---

# Direct Generation Strategy for Erdos C5

## Core Principle
Create valid step functions from scratch with integral(h)=1, bypassing the seed's broken optimizer.

## Step-by-Step Workflow

1. CALL step_function_generator to create 3-5 diverse step functions
   - Use pattern_type: bipartite, multi_modal, or sparse
   - Each satisfies integral=1 by construction

2. CALL probe_solution on each candidate
   - Screen for c5_bound < 0.381
   - Keep the best 1-2

3. CALL evaluate_solution on selected candidates
   - If combined_score > 1.0, finish

4. If no improvement, REPEAT with different patterns
   - Try bipartite, then multi-modal, then sparse
   - Adjust threshold_or_peaks and n_steps

## Key Rules
- ALWAYS start with step_function_generator
- NEVER trust the seed's optimizer - it has bugs (Pattern 14 incomplete)
- Use probe_solution before full evaluation
- Evaluate only candidates with c5_bound < 0.381
