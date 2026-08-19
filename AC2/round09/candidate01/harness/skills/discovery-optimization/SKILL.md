---
name: discovery-optimization
description: "Optimize step-functions for C2 inequality. Use step_probe to search parameter space, then evaluate the best variant. Focus on interval positions, heights, and pattern types."
---

# Step-Function C2 Optimization Strategy

Your mission: beat the seed score of 1.03431 by discovering better step-function patterns.

## Understanding the Problem

The C2 inequality constant is maximized by finding non-negative functions f where:
C2 = ||f ★ f||₂² / ((∫f)² ||f ★ f||_∞)

The seed uses multi-level step functions with:
- num_intervals: 400 discretization points
- Pattern types: high-peak single, multi-level, pyramid, asymmetric, etc.
- Heights: typically 1.4-2.2 range
- Optimizes with gradient descent over 37000 steps

## Strategy

1. **Use step_probe extensively**: This tool will test MANY parameter variations cheaply.
   - Call it with different pattern types
   - Try varying interval ratios (0.25, 0.28, 0.30, etc.)
   - Try different height values (1.42, 1.52, 1.62, 1.72, 1.92, 2.12, etc.)
   - Test pyramid shapes, multi-step, asymmetric patterns

2. **Call step_probe at least 5-10 times** before using evaluate_solution
   - Each call tests a different parameter regime
   - Note which variations get the highest C2
   - Build a picture of promising regions

3. **Make targeted edits** based on probe results
   - If pyramids work best, focus on pyramid parameters
   - If certain heights dominate, explore that height range
   - If interval ratios matter, test finer granularity

4. **Use evaluate_solution sparingly**
   - Only for your BEST candidate after thorough probing
   - You have ~30 evaluations total
   - Wasting 5 evaluations on random edits when you have probes is foolish

5. **Common successful patterns to test**:
   - Pyramid: low-higher-highest-higher-low
   - Multi-level: 3-4 levels with ascending/descending heights
   - Asymmetric: different left/right heights
   - Single high peak with wings
   - Two-step: two separate high regions

## Example Edits

Change interval ratios: "start = int(0.25 * n)" → "start = int(0.30 * n)"
Change heights: "set(1.92)" → "set(2.02)"
Add new pattern: insert a new elif branch with different structure

## When to Stop

- After 8-10 probe calls showing consistent patterns
- When evaluate_solution returns score > 1.03431
- When you've exhausted 25-30 total evaluations

CRITICAL: The seed already found a very good solution. To beat it, you need systematic exploration of the parameter space, not random edits. Use step_probe to guide your search.
