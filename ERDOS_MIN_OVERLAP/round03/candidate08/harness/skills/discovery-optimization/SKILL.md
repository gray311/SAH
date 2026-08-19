---
name: discovery-optimization
description: "Internal parameter search over Golomb ruler and bimodal constructions for Erdos minimum overlap optimization using phased training."
---

# Erdos Minimum Overlap - Internal Search Strategy

## Why Internal Search is Critical

The seed program's initialization is static. To beat C5 <= 0.380923, we need to SEARCH over Golomb ruler parameterizations (mark count 3-8, positions via local search, kernel types Gaussian/boxcar, widths 0.08-0.18).

## Method: internal_golomb_search

This tool performs a bounded internal search over Golomb-based constructions:

### Search Dimensions:
1. Number of marks: Try 3, 4, 5, 6, 7, 8 marks
2. Mark positions: For each mark count, use local search to optimize positions
   - Start from optimal Golomb ruler positions
   - Perturb and evaluate using ctx.probe()
   - Keep top 3 position sets
3. Kernel types: Gaussian vs top-hat (boxcar)
4. Kernel widths: Search over a range, normalize to ensure integral=1

### Internal Workflow:
- For each mark count (3-8):
  - Generate optimal Golomb ruler positions
  - For each kernel type (Gaussian, boxcar):
    - Search over 3 kernel widths (0.08, 0.12, 0.18)
    - For each width:
      - Run local search over positions (15 steps of perturbation and probe evaluation)
      - Keep best position set
- Return the best construction with parameters

## Optimization Integration: Phased Training

After obtaining constructions, run phased optimization:

Phase 1 (Exploration, 10000 steps):
- Learning rate: 0.05
- Penalty strength: 1000
- Goal: Escape local minima

Phase 2 (Refinement, 15000 steps):
- Learning rate: 0.01
- Penalty strength: 5000
- Goal: Fine-tune the solution

Phase 3 (Fine-tuning, 5000 steps):
- Learning rate: 0.001
- Penalty strength: 20000
- Goal: Enforce integral constraint and precision

## Tool Usage
- Use internal_golomb_search() at the start
- Extract construction parameters
- Run phased optimization
- Use probe_solution to quickly check c5_bound before final evaluation
- Evaluate top 2 candidates with evaluate_solution

## Key Principles
- Search over PARAMETERS, not just fixed patterns
- Use probe_solution for rapid candidate ranking during search
- Phase-based optimization balances exploration and exploitation
- The best construction may have non-standard mark spacing or kernel width
