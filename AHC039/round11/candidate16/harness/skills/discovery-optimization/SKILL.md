---
name: discovery-optimization
description: "Aggressive 8-direction corridor expansion with combination probing, lenient stop criteria (-3 instead of -2), larger hill climbing shifts (up to \u00b180), 25 phased restarts including local mutations."
---

# Aggressive Corridor Expansion Strategy with Combination Probing

## Phase 1: Aggressive Grid Analysis
- Use 200x200 grid with cell_size=500 (covers 0-100000)
- Count mackerels (M) and sardines (S) in each cell
- Compute cell score = M - S
- Identify top 20 cells with highest score (include negative scores if they might be useful connectors)

## Phase 2: 8-Direction Corridor Expansion
For each top cell, expand in ALL 8 directions:
- Cardinal: N (row-1), S (row+1), E (col+1), W (col-1)
- Diagonal: NE (row-1, col+1), NW (row-1, col-1), SE (row+1, col+1), SW (row+1, col-1)

For each direction:
- Start from seed cell and move outward step by step
- Continue if: cell in bounds AND (M - S) > -3 (lenient)
- Stop if: (M - S) < -10 or grid boundary
- Record corridor path

## Phase 3: Combination Probing
For each seed cell with multiple corridors:
- Generate 10-15 different corridor combination configurations
- Use probe_corridor_combinations tool to score each combination cheaply
- Each probe returns approximate M-S score
- Select top 3 combinations for full evaluation

## Phase 4: Aggressive Hill Climbing
For each candidate polygon:
- Perform 5 rounds of refinement
- For each edge, try shifts: ±5, ±10, ±20, ±40, ±80 units
- Use grid-based rectangle query for fast scoring
- Keep shift that maximizes M - S

## Phase 5: Multi-Phase Restarts
- Run 25 restarts total
- Phase 1 (restarts 0-9): Standard corridor expansion
- Phase 2 (restarts 10-19): Corridor + vertex swap mutations
- Phase 3 (restarts 20-24): Aggressive expansion with large shifts

## C++ Implementation Notes
- Use fixed-size 200x200 grid array for O(1) access
- Pre-compute all cell scores in O(N)
- Rectangle query = sum of grid cells covering rectangle
- Total time per evaluation: < 2.0s with efficient operations
- Use std::random_device for seed generation
- Include KVH polygon self-intersection check
