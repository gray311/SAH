---
name: internal-search-strategy
description: Load this skill to implement an internal multi-candidate search within each evaluation. The solver must generate multiple function variants, compute their C2 scores, and return the best one. This is essential for beating the seed score.
---

# Internal Search Strategy: Multi-variant C2 Optimization

## Why This Is Essential
The seed program scores 1.03431 using a fixed pattern. To beat this, you must NOT just tweak ONE function.
You must implement an internal search loop that explores MULTIPLE functions per evaluation and returns the best.

## Implementation Steps

Step 1: Study the seed's pattern system
The seed has _create_step_initializer(n, pattern_idx) with pattern_idx 0-12+. Each creates a different step function.
Your search loop should iterate through these patterns AND add variations.

Step 2: Build your search loop
Inside your optimized EVOLVE-BLOCK, implement:

def search_best_variant(self):
    best_f = None
    best_c2 = -1e9
    n = self.hypers.num_intervals
    
    # Try all seed patterns plus variations
    for pattern_idx in range(20):  # Try more than just 0-12
        f = self._create_step_initializer(n, pattern_idx)
        f_nn = jax.nn.relu(f)
        c2 = self._compute_c2(f_nn, n)
        if c2 > best_c2:
            best_c2 = c2
            best_f = f
    
    # Also try random variations
    for _ in range(10):
        f_random = self._random_pattern(n)
        f_nn = jax.nn.relu(f_random)
        c2 = self._compute_c2(f_nn, n)
        if c2 > best_c2:
            best_c2 = c2
            best_f = f_random
    
    return best_f, best_c2

Step 3: Ensure numerical stability
- Always apply jax.nn.relu(f) to ensure f(x) >= 0
- Handle edge cases (empty arrays, NaN, infinity)
- Keep your search loop under 5 seconds (limit patterns, use FFT)

Step 4: Return only the best variant
The evaluator expects a single function. Your search loop must find the winner and return ONLY that.

## Common Pitfalls

- Memory errors: Dont try too many patterns. Use range(10-20) not range(1000).
- Timeouts: Each evaluation has a time limit. Optimize your loop.
- Wrong output: Returning a list instead of a single function will cause validity=0.
- Not searching: Just tweaking the seed pattern will score ~1.0. You MUST search.

## Search Space to Explore

1. Original patterns: pattern_idx 0-12 (seed patterns)
2. Height variations: Change the 2-3 decimal heights
3. Width variations: Change start/end positions
4. Multi-level: Create 3-4 level patterns
5. Asymmetric: Patterns that are not symmetric around center
6. Pyramid variants: High center with lower sides

## Evaluation Budget Strategy

With 30 evaluations, structure your search like this:
- Evaluations 1-5: Baseline (seed patterns only)
- Evaluations 6-15: Height/width tweaks
- Evaluations 16-25: Multi-level and asymmetric patterns
- Evaluations 26-30: Final refinements on best approach

Key insight: The best harness does not find magic patterns through random edits. It systematically explores a search space
and returns the winner. Implement this search loop in your EVOLVE-BLOCK.
