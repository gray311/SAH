---
name: discovery-optimization
description: "Construct diverse step functions analytically (bipartite, multi-step, symmetric, sparse) with integral constraint. Use FFT to compute c5_bound. Initialize optimizer from good initializations rather than random. Focus on mathematical structures that minimize overlap."
---

# Analytical Step Function Construction for Erdos C5

## Core Principle
Don't rely on the optimizer to discover good initial h functions from random noise. Instead, CONSTRUCT diverse step functions analytically that satisfy the integral constraint, then use the optimizer for fine-tuning.

## Why This Works
- Random initializations rarely have integral ≈ 1
- Optimizer starting from bad points wastes budget
- Mathematical constructions (bipartite, Golomb, etc.) are known to give low overlap
- We can guarantee integral = 1 in the construction

## Step 1: Construct Analytical Candidates

Choose ONE construction type per iteration:

### A. Bipartite Construction
h(x) = 1 for x < a, h(x) = 0 for x >= a
To satisfy integral(h) = 1: width * 1 = 1, so width = 1. Choose a = 0.5.
This gives: h(x) = 1 if x < 0.5, else 0.
Compute c5_bound via FFT.

### B. Two-Step Construction
h(x) = 1 for x < a1, h(x) = b for a1 <= x < a2, h(x) = 0 otherwise
Choose a1, a2, b to satisfy integral = 1.
Example: a1 = 0.4, a2 = 0.6, b = 0.5 → integral = 0.4*1 + 0.2*0.5 = 0.5 (adjust as needed)

### C. Multi-Step (n peaks)
Place n narrow rectangular peaks at positions x1, x2, ..., xn
Each peak: height = H, width = w
integral = n * H * w = 1
Choose H, w, and positions to minimize overlap.
Example: 3 peaks at 0.4, 1.0, 1.6 with H=10, w=0.05 → integral ≈ 3*10*0.05 = 1.5 (normalize)

### D. Symmetric Construction
h(x) = h(2-x) (symmetric around x=1)
Use this to exploit symmetry in the overlap integral.

### E. Sparse Construction
Most of h is 0, with narrow high peaks.
This minimizes overlap because peaks rarely align.

## Step 2: Validate Construction
1. Check integral(h) ≈ 1 (should be exact by construction)
2. Check h(x) in [0,1] for all x
3. Compute c5_bound via FFT (fast, analytical)
4. If c5_bound < 0.375, proceed to optimization

## Step 3: Initialize Optimizer
If you have a constructed h with c5_bound < 0.375:
- Use edit_solution to set the EVOLVE-BLOCK with this h as INITIALIZATION
- OR, better: modify the seed program to use your constructed h as the starting point
- Run the optimizer from this GOOD starting point

## Step 4: Fine-Tuning (Optional)
If you want to fine-tune your construction:
- Use the optimizer with small learning rate
- Keep the structure (don't let it destroy your good construction)

## Step 5: Alternative Constructions
If current construction fails:
- Try bipartite with different split point
- Try different number of peaks
- Try different peak positions (Golomb-like spacing)
- Try different symmetry types

## Key Rules
- ALWAYS construct analytically first, don't rely on random initialization
- GUARANTEE integral = 1 in your construction
- Use FFT to compute c5_bound (fast, separate from optimizer)
- Only run optimizer on constructions with c5_bound < 0.375
- Try multiple construction types (bipartite, multi-step, symmetric, sparse)
- Don't waste optimizer budget on random starts
