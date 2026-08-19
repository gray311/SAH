---
name: direct-construction-strategy
description: Build explicit step functions for the Erdős C₅ problem. Don't use gradient descent. Manually construct piecewise constant functions with few breakpoints.
---

# Direct Construction Strategy for C₅ Minimum Overlap

## The Core Idea

Instead of optimizing a latent vector with Adam for 59,000 steps (which gets stuck),
construct explicit step functions directly. The C₅ objective rewards specific
structural properties that can be built by hand.

## Key Patterns to Construct

### Pattern 1: Uniform with Compact Support
- h = c on [0, a], h = 0 on [a, 2]
- Constraint: c * a * 2 = 1 (integral over [0,2])
- This creates a single "bump" of constant height

### Pattern 2: Two-Plateau Symmetric
- h = a on [0, b], h = c on [1, 2], h = 0 elsewhere
- Symmetric around x=0.5 and x=1.5
- Allows separation of mass into two non-overlapping regions

### Pattern 3: Concentrated Mass
- h = 1 on [0.5, 1.5], h = 0 elsewhere (if integral permits)
- Maximum concentration of the function in the middle

### Pattern 4: Alternating Blocks
- h = different constant values on alternating intervals
- Can create interference patterns that reduce overlap

### Pattern 5: Three-Part Structure
- Low on [0, 0.5], High on [0.5, 1.0], Low on [1.0, 2]
- Triangle-like shape

## Construction Algorithm

1. Choose a pattern from the above
2. Define step positions (breakpoints)
3. Set initial heights for each interval
4. Normalize to satisfy ∫h = 1 over [0,2]
5. Clip to [0,1] if needed (may require renormalization)
6. Compute c₅_bound using FFT correlation
7. Try multiple parameter variations of the same pattern

## Why This Works

- The optimizer in the seed explores a continuous high-dimensional space randomly
- Direct construction explores a low-dimensional manifold of structured functions
- The C₅ objective likely has "valleys" that structured functions can slide into
- Random noise (latent + Adam) smears out these valleys
- Step functions with few breakpoints can find the right "shape" precisely

## Practical Tips

- Start with 100 intervals, not 800
- Test 5-10 different constructions per evaluation
- Use probe_solution to rank before full evaluation
- If a pattern fails normalization, try adjusting heights
- Always verify: 0 ≤ h[i] ≤ 1 and |∑h[i]·dx - 1| < 0.01
