---
name: discovery-optimization
description: "Optimize axis-aligned polygon construction for NP-hard geometric problems. Implement binary search rectangle optimization: find mackerel bounding box, then shrink each dimension via binary search to exclude sardines while maximizing score."
---

# Binary Search Rectangle Optimizer for Fish Capture

## Problem
Maximize: mackerels_in - sardines_in + 1
Constraints: axis-aligned polygon, integer coords 0-100000, perimeter <= 400000, vertices <= 1000

## Core Algorithm: Binary Search Each Boundary

### Step 1: Compute Base Bounding Box
Iterate all mackerels to find:
- min_x, max_x (min/max x-coordinates)
- min_y, max_y (min/max y-coordinates)

### Step 2: Count Fish in Rectangle
pair<int,int> count_in_rect(int lx, int rx, int by, int ty) {
    int m = 0, s = 0;
    for (auto& p : mackerels) if (lx <= p.x && p.x <= rx && by <= p.y && p.y <= ty) m++;
    for (auto& p : sardines) if (lx <= p.x && p.x <= rx && by <= p.y && p.y <= ty) s++;
    return {m, s};
}

### Step 3: Binary Search Each Boundary

Shrink Left (find optimal left boundary):
- Binary search lx from min_x to max_x
- For each candidate, compute score = mackerels_in_rect - sardines_in_rect + 1
- Keep the lx that maximizes score

Repeat for Right (max_x), Bottom (min_y), Top (max_y):
- Same binary search pattern for each dimension

### Step 4: Greedy Combination
- Try shrinking each side independently
- Take the best single-sided result
- Optionally test 2-sided combinations if they improve

### Step 5: Output Rectangle Vertices
cout << 4 << "\n" << lx << " " << by << "\n";
cout << rx << " " << by << "\n";
cout << rx << " " << ty << "\n";
cout << lx << " " << ty << "\n";

## Performance
- Counting: O(N) per call
- 4 boundaries x ~13 binary search steps x O(N) each
- Total: ~0.05-0.1s for N=5000, well within 2.0s limit

## Optimization Tips
- Pre-sort fish by x and y for O(log N) range queries
- Use stride-based coarse scan followed by binary search refinement
- Parallelize boundary searches if possible

## Edge Cases
- All fish same position: output single point
- No sardines: full mackerel bounding box is optimal
- Many sardines: aggressive shrinking may be needed
