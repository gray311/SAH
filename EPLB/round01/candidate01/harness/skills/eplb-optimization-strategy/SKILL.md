---
name: eplb-optimization-strategy
description: Domain-specific playbook for optimizing MoE EPLB load-balancing algorithms.
---

# EPLB Algorithm Optimization Playbook

## Objective
Maximize score by improving load balancing and execution efficiency.

## Key Strategies

### 1. Vectorize All Loops
Convert Python for-loops to torch operations.

### 2. Pre-compute Indices
Use torch.arange and modulo-based assignment.

### 3. Sort-Based Assignment
Sort once with torch.sort, then assign.

## Process
1. Call analyze_algorithm
2. Call vectorize_transformation with pattern
3. Apply transformation
4. Evaluate and adjust
