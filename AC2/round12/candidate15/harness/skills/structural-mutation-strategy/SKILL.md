---
name: structural-mutation-strategy
description: Focus on STRUCTURAL changes to escape local optima. Small parameter tweaks won't work. Prioritize - level count changes, symmetry breaking, width scaling, height scaling.
---

# Structural Mutation Strategy for C₂ Maximization

## Why Structural Changes Are Needed

The seed program's patterns are locally optimized. Small tweaks (±0.05 on heights, 5% on widths) cannot escape these local optima. You need STRUCTURAL changes that alter the fundamental pattern class.

## Structural Mutation Categories (in order of priority)

### 1. Height Scaling (High Priority)
- Multiply ALL heights by a factor of 1.08-1.20
- This changes the relative weighting of all levels uniformly
- Can improve the L2/∞ ratio by balancing the convolution profile

### 2. Width Scaling (High Priority)
- Expand or contract intervals by 15-25% (not 5-10%)
- Focus on expanding the "core" interval(s) where the function is highest
- Wider intervals increase convolution overlap, boosting ||f★f||₂²

### 3. Level Count Changes (Very High Priority)
- Add a level: split an existing interval and introduce a new height
- Remove a level: merge two adjacent levels
- This fundamentally changes the pattern class!
- A 5-level → 6-level or 4-level change is much more promising than tweaking heights

### 4. Symmetry Breaking Type 2 (Medium Priority)
- Instead of random asymmetry, create a gradient: left side higher, right side lower
- Or: make the asymmetry position-dependent (more asymmetric at one end)
- This breaks symmetry in a more systematic way

### 5. Multi-Peaked Creation (Medium Priority)
- If current pattern has ≤3 levels, create a 4-level pattern with two distinct peaks
- If already multi-peaked, add a narrow high peak in the center
- More peaks = more degrees of freedom in the convolution profile

## Execution Protocol

1. Call diversity_generator ONCE at start to get 5 distinct proposals
2. For EACH proposal type (try to keep them distinct):
   - Implement with edit_solution (make LARGE changes)
   - Evaluate with evaluate_solution
   - If improvement: generate 3-5 more variants of THIS mutation type
   - If 2 failures: switch to a DIFFERENT mutation type immediately
3. After exhausting 4-5 mutation types without success, try entirely new architectures
4. NEVER stick with one mutation type after 2 failures

## Key Principle

STRUCTURE > PARAMETERS. A 5-level → 6-level change is more powerful than tweaking heights by 0.05.
