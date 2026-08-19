---
name: discovery-optimization
description: "Fix and optimize C++ code for fish-capture optimization. Focus on compiling first, then implement grid-based rectangle search. Use evaluate_solution sparingly."
---

# Fixing and Optimizing C++ for Fish Capture

## Critical: Fix Compilation First
The seed C++ code may have errors. Check:
- All #includes present: iostream, vector, algorithm, chrono, random, set, etc.
- main() returns int
- Output format: exactly m\n coords (no extra text)
- No syntax errors in loops, conditionals, function calls

## Grid-Based Fish Counting
Code pattern:
const int CELL_SIZE = 50;
vector<vector<int>> grid(2001, vector<int>(2001, 0));

// Build grid
for (const auto& f : all_fish_structs) {
    int gx = min(2000, f.p.x / CELL_SIZE + 1);
    int gy = min(2000, f.p.y / CELL_SIZE + 1);
    grid[gx][gy] += f.type;
}

// Count in rectangle
int count_rect(int minx, int maxx, int miny, int maxy) {
    int sum = 0;
    for (int x = minx; x <= maxx; x += CELL_SIZE) {
        for (int y = miny; y <= maxy; y += CELL_SIZE) {
            sum += grid[x/CELL_SIZE][y/CELL_SIZE];
        }
    }
    return sum;
}

## Rectangle Search
1. Find mackerel centroid: sum all mackerel x, divide by count
2. Generate candidates:
   for (dx = -200 to 200 step 50) {
     for (dy = -200 to 200 step 50) {
       for (size in {200, 300, 400}) {
         minx = cx + dx - size/2, maxx = cx + dx + size/2
         miny = cy + dy - size/2, maxy = cy + dy + size/2
         score = count_rect(minx, maxx, miny, maxy)
         if (perimeter_ok) candidates.add(score, minx, maxx, miny, maxy)
       }
     }
   }
3. Sort by score descending, keep top 3
4. Evaluate top 3 with evaluate_solution
5. Output best

## Common Bugs
- Wrong output format: must be exactly m\n coords
- Perimeter > 400000: check before output
- Coordinates out of range: clamp to 0-100000
- Not compiling: check all brackets, semicolons, function signatures

## Evaluation Strategy
- Use probe_solution if available for fast scoring during search
- Use evaluate_solution only for final 1-2 candidates
- If validity=0, fix the C++ code and retry
- If score < expected, try different search parameters
