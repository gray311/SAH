---
name: hex-pack-complete-guide
description: Complete guide to hexagonal circle packing with the hexagonal_construction tool.
---

COMPLETE GUIDE: Hexagonal Circle Packing with Tool Integration
OBJECTIVE: Beat seed score 0.947992 using hexagonal (staggered) packing.
THE TOOL IS YOUR FRIEND: The hexagonal_construction tool generates the ENTIRE construct_packing() function ready to use. No code writing required - just call the tool and replace EVOLVE-BLOCK.
STEP-BY-STEP WORKFLOW:
1. CALL THE TOOL: hexagonal_construction(row_counts=[5,5,5,5,6])
2. COPY OUTPUT: Take the complete code from the tool response
3. REPLACE EVOLVE-BLOCK: Paste into edit_solution. It must be the ONLY code in the block.
4. PROBE: Use probe_solution to check the score (should be > 0.95)
5. EVALUATE (if probe is good): Use evaluate_solution for final score
WHY HEXAGONAL IS BETTER: - Square grid (seed): circles in perfect rows, 20% wasted space - Hexagonal: odd rows shifted by half-spacing, ~90.69% density - For n=26 in unit square, hexagonal can reach sum_radii ~2.635
CORRECT PARAMETERS: - spacing = 0.1667 (not 0.20!) - x_start even rows = 0.05 - x_start odd rows = 0.0833 - row_y = [0.10, 0.30, 0.50, 0.70, 0.90] - row_counts = [5,5,5,5,6]
CUMULATIVE INDEXING (CRITICAL): The tool uses cumulative indexing: cumulative = 0 for each row: for each circle in row: centers[cumulative] = [x, y] cumulative += 1
This is DIFFERENT from the buggy seed pattern: centers[row_idx * num_rows + i]  # WRONG!
PROBING FIRST: - Always use probe_solution before evaluate_solution - Probe is cheap (10s vs minutes), has 30 budget - Evaluate only if probe shows promise
TROUBLESHOOTING:
Score still low? - Verify you used the COMPLETE code from the tool - Check odd rows have x_start = 0.0833 - Check spacing = 0.1667 - Verify cumulative indexing is present
Tool output looks wrong? - The tool should generate construct_packing() with build_hexagonal_grid() inside - If you see just build_hexagonal_grid() without construct_packing(), you did it wrong
Remember: The tool does everything. Just call it, copy, paste, probe, evaluate.
