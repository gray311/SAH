---
name: discovery-optimization
description: "Optimize C++ polygon construction for fish-capture maximization. Use\nanalyze_mackerel_clusters to find dense mackerel regions, then build\naxis-aligned polygons around these clusters while excluding nearby sardines.\nImplement stepped/L-shaped polygon constructors and systematic local refinement."
---

# Cluster-Based Polygon Optimization

## Phase 1: Analyze Mackerel Clusters (MANDATORY FIRST STEP)
- Call analyze_mackerel_clusters to get:
  - Top 5-10 dense mackerel clusters with centroids
  - Cluster densities (mackerels per unit area)
  - Distance to nearest sardines for each cluster
- Sort clusters by density / sardine-proximity ratio
- Select top 2-3 clusters as primary targets

## Phase 2: Build Targeted Polygons
For each selected cluster:
- **Rectangular baseline**: Bounding box of cluster ± margin
- **Stepped polygon**: Create staircase around cluster edges to exclude nearby sardines
- **L-shaped variant**: If sardines form a line, use L-shape to step around them
- Calculate score for each variant using grid counting

## Phase 3: Multi-Cluster Combination
- Try combining top 2 clusters with a connecting rectangle
- Score the combined polygon
- If beneficial, keep the combined shape

## Phase 4: Local Refinement
- From best polygon, perturb each edge by ±1 to ±10 units
- Keep modifications that increase score
- Try up to 100 refinements within time budget

## Phase 5: Time Budget Management
- 0.1s: Cluster analysis
- 0.3s: Baseline polygon construction
- 0.5s: Advanced shape variants (stepped, L-shaped)
- 0.8s: Local refinement
- 0.3s: Final validation
- Always output a VALID polygon even if score is suboptimal

## C++ Implementation Patterns
```cpp
// Grid-based fast counting
int count_in_rect(int minX, int maxX, int minY, int maxY) {
    int count = 0;
    for (int x = minX; x <= maxX; x++) {
        for (int y = minY; y <= maxY; y++) {
            if (is_inside(x, y)) count++;
        }
    }
    return count;
}

// Stepped polygon around cluster
vector<Point> make_stepped_polygon(const vector<Point>& cluster, const vector<Sardine>& nearby) {
    // Create staircase pattern that follows cluster boundary
    // Indent inward near sardines
}
```
