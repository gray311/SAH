You are solving an NP-hard fish-capture polygon optimization problem.

Goal: Maximize (mackerels_inside - sardines_inside + 1) with an axis-aligned, non-self-intersecting polygon.

CRITICAL CODE REQUIREMENTS:
1. Build a GRID INDEX (100x100 cells, 1000x1000 units each) for O(1) fish counting
2. Implement THREE polygon constructors: simple_rect(), l_shape_top_right(), stepped_enclose()
3. Implement iterative refinement: perturb each vertex by ±1 to ±10, keep best
4. Use time-budgeted search: run for ~1.8s, always output valid polygon on exit
5. Sardine avoidance is CRITICAL - indent edges near sardine clusters

SEARCH LOOP (must be in main()):
- t0: Build grid index from all fish (~0.05s)
- t1: Generate 20 random seed polygons (~0.3s)
- t2: For each of top 10, try 50 refinements (~0.7s)
- t3: Try 5 L-shapes and 5 stepped polygons (~0.4s)
- t4: Final polish with greedy edge moves (~0.35s)
- Always stop before 2.0s, output valid polygon

Grid indexing pattern:
```cpp
int CELL_SIZE = 1000;
int GRID_SIZE = 100;
struct GridCell { int mackerels = 0, sardines = 0; };
GridCell grid[GRID_SIZE][GRID_SIZE];

void build_grid() {
    for (int i = 0; i < 2*N; i++) {
        int cx = min(all_fish[i].x / CELL_SIZE, GRID_SIZE - 1);
        int cy = min(all_fish[i].y / CELL_SIZE, GRID_SIZE - 1);
        if (all_fish[i].type == 1) grid[cx][cy].mackerels++;
        else grid[cx][cy].sardines++;
    }
}

int count_in_rect(int minX, int maxX, int minY, int maxY) {
    int cx0 = minX / CELL_SIZE, cy0 = minY / CELL_SIZE;
    int cx1 = max((maxX+1)/CELL_SIZE - 1, 0), cy1 = max((maxY+1)/CELL_SIZE - 1, 0);
    int m=0, s=0;
    for (int cx = cx0; cx <= cx1; cx++) for (int cy = cy0; cy <= cy1; cy++) {
        m += grid[cx][cy].mackerels; s += grid[cx][cy].sardines;
    }
    return m - s;
}
```

Output format: m vertices, each "x y", all distinct, axis-aligned edges, non-self-intersecting, perimeter <= 400000.

DO NOT output a fixed/static polygon. The code must actively search within time limits.
