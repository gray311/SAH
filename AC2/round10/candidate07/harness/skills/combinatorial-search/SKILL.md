---
name: combinatorial-search
description: Explore C₂ through COMBINATORIAL pattern rearrangements. Use restructure_steps to merge/split steps, create new architectures, probe before evaluate.
---

# C₂ Combinatorial Search

## Key Point
Current patterns are LOCAL OPTIMA. Must REARRANGE structure, not tweak parameters.

## Protocol

### Phase 1: Initial Restructuring (Iter 1-5)
Call restructure_steps with different edit_types: merge, split, reorder, reshape, retune.
For each: call probe_solution, compare to best, mark promising if probe > best.

### Phase 2: Exploration (Iter 6-30)
Continue restructuring promising variants. Try 3-5 restructures per direction.
Only evaluate when probe beats baseline.

### Phase 3: Diversification (If Stuck)
After 10 iterations without improvement, try DIFFERENT pattern class:
- Bimodal peaks
- Multi-plateau
- Skewed distributions
- Gaussian-like

### Phase 4: Refinement (If Near Success)
Fine-tune boundaries and heights. Still probe before evaluate.

## Rules
1. DON'T just tweak ±5%
2. MUST call restructure_steps at start
3. ALWAYS probe before full evaluate
4. Evaluate only promising variants
5. If stuck, CHANGE pattern class
