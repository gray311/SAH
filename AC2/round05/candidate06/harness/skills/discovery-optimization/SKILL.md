---
name: discovery-optimization
description: "Deeply optimize piecewise-linear representation before exploring alternatives. Use analyze_convolution to diagnose limitations, then systematically refine intervals, learning rate, and step count. Probe 3+ variants before eval."
---

# C2 Optimization: Deep Refinement Strategy

## Core Principle
The seed program (piecewise-linear, 400 intervals, lr=0.25, 30k steps) achieves 1.02665. This is near-optimal. Do NOT jump to step functions or other families until you've exhausted refinements to the current approach.

## Phase 1: Diagnostic Analysis
1. Call analyze_convolution to understand:
   - Current function shape (peaks, flat regions, support width)
   - Convolution properties (peak location, tail behavior)
   - Integration error estimates (from discretization)
2. Identify bottleneck: Is it discretization error? Optimization convergence? Function shape?

## Phase 2: Systematic Refinement
For EACH parameter, test 3-5 values using probe_solution:

### A. Discretization (num_intervals)
- Values: [500, 800, 1200, 1600, 2000]
- Expectation: Finer grids reduce integration error, may improve C2
- Probe all 5 before eval

### B. Learning Rate Schedule
- Values: [0.1, 0.15, 0.2, 0.25, 0.3]
- Expectation: Different lrs may converge to better minima
- Test with warmup_steps=3000, then cosine decay

### C. Optimization Duration
- Values: [30000, 50000, 80000, 100000]
- Expectation: More steps may refine solution further

### D. Multi-start Variants
- Keep 9 initializations but vary their positions/widths
- Probe 3 variants per seed

## Phase 3: Evaluate and Decide
1. Pick top 2 from probes
2. Run full evaluation on each
3. If no improvement (>10k steps or 3 evals): THEN try step functions

## Critical Rules
- Probe 3+ variants BEFORE any eval
- Do NOT explore new families until current approach fails
- Finer discretization is your first lever, not architectural changes
- Use analyze_convolution at least twice: start and after refinement
