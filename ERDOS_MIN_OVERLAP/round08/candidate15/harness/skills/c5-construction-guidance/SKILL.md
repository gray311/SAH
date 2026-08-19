---
name: c5-construction-guidance
description: Guide step function construction for C₅ problem. Focus on simple, analytically justified families.
---

# C₅ Construction Guidance

## Key Insight
The trivial solution h=1 on [0,1], h=0 elsewhere gives c5_bound = 1/3 ≈ 0.3333.
This yields combined_score ≈ 1.14, which beats the current record of 1.0!

## Construction Templates

### Template 1: Single Block (SHOULD WORK!)
h(x) = 1 for x ∈ [0, 1], 0 otherwise
- Integral is automatically 1
- c5_bound = 1/3
- Implementation: Create array with 1s in [0,1], 0s elsewhere

### Template 2: Two Symmetric Blocks
h(x) = α for x ∈ [0, b] ∪ [2-b, 2], 0 otherwise
- α = 1/(2b) ensures ∫h = 1
- Try b = 0.5: α = 1 (same as single block)
- Try b = 0.75: α = 2/3 ≈ 0.667

### Template 3: Three-Block Symmetric
h(x) = α for x ∈ [0, a] ∪ [1, 1+b] ∪ [2-b, 2], 0 otherwise
- More flexibility for reducing correlations

### Template 4: Fixed-Position Multi-Block
1. Define 5-20 fixed block positions
2. Optimize just the heights (one constraint: sum of heights * widths = 1)
3. Use grid search or coordinate descent

## Implementation Tips

- Use construct_step_function tool to quickly test ideas
- Always verify integral = 1
- Start with 1-2 blocks before complex patterns
- The seed's 800-interval Adam approach may be overcomplicated
- If you find combined_score > 1.0, you're done!

## Quick Start
Try Template 1 first - it's the simplest valid solution and should beat the record.
