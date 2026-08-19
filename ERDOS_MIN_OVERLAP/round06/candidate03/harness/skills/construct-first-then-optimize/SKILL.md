---
name: construct-first-then-optimize
description: For Erdos C5 bound - manual step function constructions beat gradient descent from random. Write code that BUILDS a specific pattern, then optionally refine with optimization.
---

Construct-First Strategy for C5 Bound

Core Principle
The optimal step function likely has a SIMPLE STRUCTURE (few breakpoints, symmetric, periodic).
Don't start from random and optimize. START WITH THE CONSTRUCTION, then refine.

Step 1: Choose a Pattern Class
- Single-step: h=1 on [0,1], 0 elsewhere
- Double-step: h=alpha on [0,a] union [2-a,2], 0 elsewhere
- Symmetric tripartite: three regions with different heights
- Concentrated with gap: mass in two intervals, gap in middle

Step 2: Write Direct Construction Code
Replace the seed's _get_best_initialization with code that:
1. Defines breakpoints and heights analytically
2. Ensures integral=1 exactly (scale if needed)
3. Clamps to [0,1]

Step 3: Compute c5_bound Directly
No optimization loop needed for baseline:
h = define_your_step_function()
j = 1.0 - h
corr = fft-based correlation
c5 = max_k (h * j)_k * dx

Step 4: Optional Refinement
If baseline has combined_score > 0.95:
- Fine-tune breakpoints with small optimization
- Or try perturbation around your construction

Step 5: Rank with probe_solution
Test 3-4 construction types. Only evaluate the best 1-2 fully.

Example: Double-Step Construction
Define a=0.4. Then alpha = 1.0/(2*a) = 1.25.
Set h=1.25 on [0,0.4] and [1.6,2], h=0 elsewhere.
This is FAST, GUARANTEED integral=1, easy to vary a.
