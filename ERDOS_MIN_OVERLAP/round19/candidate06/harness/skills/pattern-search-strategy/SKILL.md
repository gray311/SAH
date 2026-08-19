---
name: pattern-search-strategy
description: Search for better Erdos C5 bounds using analytical pattern constructions that are NOT gradients of current solutions. Each pattern is a standalone initialization with precomputed scores.
---

# Pattern-Based Search for Erdos C5 Optimization

## Why Gradient Descent Fails

The seed optimizer uses gradient descent with sigmoid initialization.
This produces candidates VERY CLOSE to the seed (c5_bound ~0.3809).
Gradient descent STALLS because the landscape is flat near the current solution.

## Solution: Pattern-Based Search

We generate STANDALONE pattern constructions from combinatorial design theory:
- Golomb ruler: optimal spacing to minimize pairwise overlaps
- Bipartite: separated support reduces max overlap
- Multi-modal: multiple narrow peaks
- Uniform/step: simple analytical functions

## Workflow

1. CALL generate_structured_patterns with a SPECIFIC pattern type (e.g., golomb_5)

2. Analyze the 8 candidates:
   - Check integral (~1.0)
   - Note c5_bound (precomputed analytical score)

3. FILTER candidates:
   - SKIP if integral != 1.0 (constraint violation)
   - SKIP if c5_bound >= 0.375 (too bad)
   - KEEP all with c5_bound < 0.375

4. CALL evaluate_solution on all kept candidates (typically 2-6)

5. If none pass, try a DIFFERENT pattern type (not new random seeds)
   - golomb_7, bi_modal, sparse_4, uniform, step, etc.

6. After EACH full evaluation:
   - If any candidate beats seed, KEEP IT as new baseline
   - Generate a NEW pattern (completely different from before)

## Key Principles

- NO gradient descent: we are exploring new regions entirely
- Pattern diversity: 12 different analytical structures
- Precomputed scores: fast analytical screening
- Direct evaluation: each pattern is a complete candidate

## Expected Results

With 8 diverse patterns per batch and 2-4 evals, we can explore 30+ unique candidates.
Even if only 10% have c5_bound < 0.375, that's 3 promising candidates per batch.
