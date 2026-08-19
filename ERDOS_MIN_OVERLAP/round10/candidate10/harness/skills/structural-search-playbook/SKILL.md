---
name: structural-search-playbook
description: For Erdos overlap minimization, try discrete/combinatorial step functions first. Smooth sigmoids likely find local optima. Binary and multi-peak constructions may escape these.
---

# Structural Search for Erdos Minimum Overlap

## Core Principle
The seed optimizer finds smooth solutions. To beat C5 ≤ 0.380923, try DISCRETE
step functions: 0/1 blocks, sharp peaks, combinatorial patterns.

## Search Strategy

### Phase 1: Structural Exploration
1. Call construct_structured_init to get diverse starting points
2. Try: binary blocks, multi-peak Gaussians, periodic patterns
3. For each, EDIT to implement in the optimizer, then probe

### Phase 2: Parameter Refinement
1. Pick top 2-3 structural variants by probe score
2. EDIT to fine-tune: adjust peak positions, block widths, amplitudes
3. Evaluate the best refinements

### Phase 3: Hybrid Approaches
1. Combine binary structures with smooth transitions
2. Use multi-start optimization from discrete initializations
3. Try different penalty strengths to enforce constraints

## When to Use This
- If hyperparameter tuning fails (no improvement after 5+ variants)
- If current best score is close to seed but not better
- When you suspect the search is stuck in smooth-function regime

## Key Insight
Overlap minimization benefits from sparse, separated support regions.
Binary/multipeak functions naturally create these. Smooth sigmoids dilute this.
