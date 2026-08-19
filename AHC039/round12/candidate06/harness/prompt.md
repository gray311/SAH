You are a C++ polygon optimizer for axis-aligned fish capture. Generate CORRECT, COMPILED C++ code.

CRITICAL: The C++ program must be COMPLETE and SYNTAX-CORRECT. Any compilation error, runtime crash, or invalid output scores 0.

APPROACH: Use a template-based code generation strategy:

1. Keep the main structure from the seed program (includes, Point struct, KD-tree)
2. Add GRID-BASED SCORING as the primary method (faster, more reliable):
   - Parse fish input into a 200x200 grid (cell_size=500)
   - Count mackerels (type 1) and sardines (type -1) per cell
   - For each evaluation, build the grid once, then query rectangles efficiently
3. Use GREEDY RECTANGLE EXPANSION:
   - Find the cell with maximum (M-S) score
   - Expand greedily in 4 directions as long as it improves score
   - Convert to a valid axis-aligned polygon
4. Run multiple restarts with different starting cells
5. Output valid polygon: m vertices, each with integer coords in [0,100000]

MUST-VALIDATE CHECKS:
- Output format: first line = vertex count (4-1000), then vertices
- Polygon must be non-self-intersecting
- Perimeter <= 400,000
- Must complete within ~1.9s

Template structure to follow:
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  // Read input: N, then 2N points (mackerels first, then sardines)
  // Build grid [200][200] counting M and S per cell
  // Find best starting cell, expand greedily
  // Output polygon vertices
  return 0;
}
```

Generated code must be COMPLETE, COMPILABLE, and produce VALID output for all 150 test cases.
