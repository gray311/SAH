---
name: discovery-optimization
description: "Optimize a program's EVOLVE-BLOCK to maximize combined_score by implementing internal multi-candidate search loops\nthat generate and evaluate multiple function variants per evaluation, then return the best variant."
---

# Multi-Candidate Search Strategy for C2 Optimization

## Core Idea
Instead of trying to discover ONE optimal function through incremental edits, each EVOLVE-BLOCK must contain
an internal search loop that:
1. Enumerates multiple function configurations (different step heights, widths, placements)
2. Computes C2 for each using the convolution objective
3. Returns the function achieving the highest C2

## Implementation Blueprint

Study the seed's _create_step_initializer which uses pattern_idx (0-12+) for different step patterns.
Your EVOLVE-BLOCK should extend this with a proper search loop that:

Structure inside your EVOLVE-BLOCK:
def optimize_c2(self):
    best_f = None
    best_c2 = -1e9
    n = self.hypers.num_intervals
    
    # Try multiple pattern configurations
    for pattern_idx in range(max_variants):
        f_values = self._create_step_initializer(n, pattern_idx)
        c2 = self._evaluate_c2(f_values, n)
        if c2 > best_c2:
            best_c2 = c2
            best_f = f_values
    
    return best_f  # Return the function with highest C2

## Key Technical Points

1. Multi-variant generation: Try at least 5-10 different pattern configurations per evaluation
2. Efficient computation: Use FFT-based convolution (already in seed) for O(n log n) speed
3. Return best variant: The evaluator expects a single function; you must search internally and return the winner
4. Preserve seed patterns: Keep the seed's 13+ patterns as your starting configurations, then add variations

## Edit Strategy

- Small changes: Use SEARCH/REPLACE to modify the objective function or add a simple search loop
- Large changes: Send a full EVOLVE-BLOCK rewrite when changing from single-function to multi-candidate search
- Always preserve: imports outside EVOLVE-BLOCK, the fixed entry function signature

## When Things Go Wrong

- validity=0: The program crashed (memory error, timeout, NaN). Read the error message and fix:
  * Memory: Reduce max_variants in your search loop
  * Timeout: Simplify your search, fewer patterns
  * NaN: Ensure f(x) >= 0 using jax.nn.relu before convolution
- Lower score: Your search strategy didn't find better functions. Try different patterns or search space

## Budget Management

- You have 30 evaluations total. Each must be a distinct internal search strategy.
- Evaluation 1-5: Baseline searches (seed patterns only, different search ranges)
- Evaluation 6-15: Enhanced searches (add new pattern types, optimize heights)
- Evaluation 16-25: Specialized searches (asymmetric patterns, multi-level patterns)
- Evaluation 26-30: Final refinements on the best approach found

Remember: The score you see after each evaluation is for the BEST variant your internal search found. Your goal is to make each internal search smarter and more thorough.
