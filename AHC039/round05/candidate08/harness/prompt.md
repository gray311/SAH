You are an expert C++ algorithm engineer tasked with iteratively improving a C++ program to MAXIMIZE the performance metrics reported by an automatic evaluator. The program has a single editable region between `# EVOLVE-BLOCK-START` and `# EVOLVE-BLOCK-END` containing a CPP_CODE variable holding a C++ program. Only that region is yours to change.

TASK: Orthogonal Polygon Coverage Maximization
Objective: Maximize score = max(0, a - b + 1) where a = mackerels inside polygon, b = sardines inside polygon.
Constraints:
  - Polygon vertices: 4 to 1000, integer coords 0 to 100000
  - Each edge parallel to x or y axis
  - No self-intersections
  - Total edge length <= 400000
Input: N=5000 mackerels and 5000 sardines (total 10000 points).
Output format:
  m
  x0 y0
  x1 y1
  ...
  x_{m-1} y_{m-1}

METHOD: Bounded Internal Search with Multi-Phase Construction

Phase 1 - Initial Rapid Construction (must complete in ~0.1s):
  - Identify unique x and y coordinates from ALL mackerels (ignoring sardines initially)
  - Greedily pick up to 1000 x and y values to form a grid of candidate vertices
  - Build an initial rectangle-aligned polygon that encloses most mackerels with minimal sardines
  - Use median-based ranges to ensure good coverage of mackerel density

Phase 2 - Scored Variants Generation (must complete in ~0.7s):
  - Generate 3-5 orthogonal polygon variants:
    1. Maximum enclosing rectangle aligned to first/second most common x and y
    2. Cross pattern: square plus four rectangles extending from center
    3. Multi-lobed pattern: several rectangles sharing edges
    4. Concentric pattern: nested rectangles
  - For each variant, ensure edge length constraint is met by scaling down if needed
  - Handle the case where no fish exist by outputting a minimal 4-vertex polygon

Phase 3 - Internal Search Loop (must complete in ~1.0s, safety margin 0.05s):
  - Use a time-based while loop that explores variations until timeout
  - Start with the best variant from Phase 2
  - Try localized mutations:
    * Move vertices by +/-1 to +/-10 units along grid
    * Add/remove small rectangular appendages at vertices
    * Swap adjacent edges to create dents
    * Combine two rectangles at right angles
  - Track the best score seen internally by approximating coverage
    (use sampling or centroid inclusion for fast estimation)
  - ALWAYS break before the 1.95s hard limit (use 1.85s safety margin)

Phase 4 - Final Output:
  - Output the vertex list of the best internal-search variant
  - If no internal search happened, output the best Phase 2 variant

CRITICAL RULES:
  - The time-based search MUST be inside main() or a called function
  - Use std::chrono for timing, break when elapsed > 1.85 seconds
  - Do NOT output during search, only at the end
  - Handle edge cases: no mackerels, all mackerels coincident, impossible coverage
  - If internal search runs out of time, output whatever best-sofar you have
  - The search MUST actively improve on seed, not just use a static rectangle

VALIDATION CHECKS BEFORE OUTPUT:
  - m >= 4 and m <= 1000
  - Total perimeter <= 400000
  - All coords in [0, 100000]
  - Polygon closes (last point != first point for output)
  - Non-zero area

CALLS TO make during search:
  - Keep a best vertex list and update when a better-estimated score is found
  - You may use sampling for fast score estimation but MUST use a deterministic
    algorithm that completes within time budget
  - Do not call expensive functions that could exceed 2s total
