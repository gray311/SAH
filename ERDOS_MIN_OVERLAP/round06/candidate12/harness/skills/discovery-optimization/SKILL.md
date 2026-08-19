---
name: discovery-optimization
description: "C\u2085 optimization harness using explicit construction and metaheuristic search.\nFocus on diverse step function constructions rather than gradient optimization.\nTarget: combined_score > 1.0 via systematic pattern exploration."
---

# C₅ Bound Optimization: Construction-Based Strategy

## Problem Understanding

We want to minimize max_k ∫₀² h(x)(1-h(x+k)) dx
where h is a step function from [0,2] to [0,1] with ∫h=1.

The seed's gradient optimizer fails because:
- The loss landscape has many poor local optima
- Gradient ascent from random starts rarely finds the global structure
- The optimal solution likely has specific combinatorial structure

## Core Strategy: Construct, Don't Optimize

**DON'T** try to improve the seed's optimizer. Instead:
- Write COMPLETELY NEW candidate solutions
- Use mathematical reasoning to construct promising step functions
- Test many different structural patterns
- Keep the best constructions found

## Construction Guidelines

### Pattern 1: Symmetric Two-Step Function
h(x) = a for x ∈ [0, b], h(x) = c for x ∈ [b, 2]
- Constraint: a·b + c·(2-b) = 1
- Try different (a,c) pairs: (1,0), (0.5,0.5), (0.8,0.2), etc.

### Pattern 2: Three-Step Symmetric Function
h(x) = a for x ∈ [0, 1/3], b for x ∈ [1/3, 2/3], c for x ∈ [2/3, 2]
- Or variations with different breakpoint positions

### Pattern 3: Concentrated Mass
- Put all mass in a small interval: h(x) = 1/ε on [0, ε], 0 elsewhere
- This gives c5_bound = 1/ε (worst), but try variations

### Pattern 4: Waveform-Based Steps
- Sample a smooth waveform (sin, cos, polynomial) at discrete points
- Quantize to [0,1] and create step function
- Use specific frequencies that might minimize overlap

### Pattern 5: Binary Step Function (extreme case)
- h(x) ∈ {0,1} only
- This is the most constrained but sometimes optimal for these problems

## Search Protocol

1. **DIVERSITY FIRST**: Try at least 5-10 completely different constructions
2. **SYSTEMATIC VARIATION**: For promising patterns, vary:
   - Number of steps (2, 3, 4, 5, 6, 8, 10)
   - Breakpoint positions (rational fractions)
   - Height values (while maintaining ∫h=1)
3. **METAHEURISTIC APPROACH**: 
   - Keep track of best c5_bound seen
   - When finding a good candidate, do focused search around it
   - When stuck, restart with completely different pattern
4. **VARY NUM_INTERVALS**: Start coarse (100 intervals), refine if needed

## What to Avoid

- Small tweaks to the seed's optimizer parameters
- Trying to "fix" the existing multi-restart approach
- Expecting gradient-based methods to work well here
- Spending iterations on minor improvements without structural changes

## Success Criteria

- combined_score > 1.0 means c5_bound < 0.38092303510845016
- This requires fundamentally better constructions than the seed found
- The optimal solution likely has a specific combinatorial structure
