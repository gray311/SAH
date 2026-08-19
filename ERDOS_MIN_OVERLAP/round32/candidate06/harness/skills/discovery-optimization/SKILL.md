---
name: discovery-optimization
description: "Create step functions with narrow separated peaks to minimize overlap."
---

# Erdos C5 - Narrow Peak Strategy

## Core Idea
The optimal solution uses NARROW, SEPARATED peaks. Wider functions create more overlap with their shifts.

## Step-by-Step Construction

1. **Choose peak positions**: Pick 3-5 positions spread across [0,2]
   - Examples: [0.4, 1.0, 1.6] or [0.3, 0.8, 1.3, 1.8] or [0.5, 1.5]
   - Spacing should be ~0.5-0.7 to avoid overlap with shifts

2. **Create narrow peaks**: For each position, create a narrow region
   - Use sigmoid: h = 1 / (1 + exp(-10 * (x - peak_pos)))
   - Width should be ~0.1-0.2 (steepness parameter ~5-10)

3. **Scale to integral = 1**: Adjust peak heights so integral(h) = 1
   - If you have N peaks of width w and height H, integral ≈ N * w * H
   - Set H = 1 / (N * w) to get integral = 1

4. **Combine peaks**: Sum the individual peak functions
   - h(x) = sum over i of: sigmoid(-10 * (x - pos_i)) + sigmoid(10 * (x - pos_i))

5. **Evaluate and refine**: Check c5_bound, adjust peak spacing/width

## Example Code Pattern
