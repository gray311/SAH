---
name: discovery-optimization
description: "EPLB algorithm optimization: improve expert rearrangement for MoE load balancing, balancing quality vs speed under budget constraints."
---

# EPLB Algorithm Improvement Strategy

## Core Principles

1. **Preserve API**: Function signatures and entry points are frozen. Only change the EVOLVE-BLOCK implementation.

2. **Two objectives**: Maximize load balance quality AND minimize execution time.

3. **Bounded search**: Use bounded internal loops (e.g., limited iterations over config options).

## Improvement Directions

### A. Weighted Bin-Packing Improvements
- Try different greedy strategies (minimum items, then minimum weight)
- Consider round-robin, best-fit, first-fit variants
- Try sorting by different keys (weight, then original index)

### B. Replication Strategies
- Power-of-two rounding (replicate to powers of 2)
- Demand-aware replication (replicate high-usage experts more)
- Threshold-based replication

### C. Hierarchical Optimizations
- Group-level packing before replica-level
- Exploit NVLink topology (faster intra-node communication)
- Balance across nodes vs GPUs

### D. Performance Optimizations
- Replace Python loops with torch operations
- Pre-compute common values (avoid repeated calculations)
- Use in-place operations where safe
- Cache repeated computations

## Method

1. Read the current algorithm
2. Choose ONE improvement direction
3. Implement a BOUNDED variant (e.g., try 3-5 configs, pick best)
4. Call probe_solution to rank variants
5. If promising, call evaluate_solution
6. Iterate with new insight

## Time Awareness

- Use `time.perf_counter()` to track internal execution
- Keep internal search well under per-eval timeout
- When timeout is tight, prefer simpler algorithms

## Validity Check

- Preserve exact input/output shapes
- Handle edge cases (num_groups % num_packs == 0, etc.)
- Use device-aware code (cpu/cuda as in original)
