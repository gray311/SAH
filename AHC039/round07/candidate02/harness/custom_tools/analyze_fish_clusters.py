def run(ctx, args):
    # Read input (N=5000 mackerels + 5000 sardines)
    # Parse lines: line 1 is N, lines 2-5001 are mackerels, 5002-10001 are sardines
    
    # Read all fish positions
    lines = ctx.read_input_sample("input.txt", nrows=10001)
    lines = lines.strip().split('\n')
    
    mackerels = []
    sardines = []
    
    for i, line in enumerate(lines[1:]):
        if not line.strip():
            continue
        # Handle comma-separated coordinates if present
        parts = line.strip().split(',')
        coords = list(map(int, parts))
        if len(coords) == 2:
            mackerels.append((coords[0], coords[1]))
            if len(mackerels) >= 5000:
                break
    
    # Build a coarse grid (200x200 cells)
    cell_size = 200
    grid = {}
    
    for mx, my in mackerels:
        cx, cy = mx // cell_size, my // cell_size
        if (cx, cy) not in grid:
            grid[(cx, cy)] = {'mackerels': 0, 'sardines': 0}
        grid[(cx, cy)]['mackerels'] += 1
    
    # Mark sardines on grid
    for i in range(5000):
        if i < len(sardines):
            sx, sy = sardines[i]
            cx, cy = sx // cell_size, sy // cell_size
            if (cx, cy) in grid:
                grid[(cx, cy)]['sardines'] += 1
    
    # Find promising clusters
    clusters = []
    visited = set()
    
    for (cx, cy), counts in grid.items():
        if counts['mackerels'] > 2 and counts['sardines'] == 0 and (cx, cy) not in visited:
            # BFS to find connected component
            cluster_cells = [(cx, cy)]
            visited.add((cx, cy))
            q = [(cx, cy)]
            
            while q:
                curr_cx, curr_cy = q.pop(0)
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    ncx, ncy = curr_cx + dx, curr_cy + dy
                    if (ncx, ncy) not in visited and (ncx, ncy) in grid:
                        if grid[(ncx, ncy)]['mackerels'] > 2 and grid[(ncx, ncy)]['sardines'] == 0:
                            visited.add((ncx, ncy))
                            cluster_cells.append((ncx, ncy))
                            q.append((ncx, ncy))
            
            # Compute bounding box of cluster
            min_x = min(m * cell_size for m, _ in cluster_cells)
            max_x = max((m + 1) * cell_size for m, _ in cluster_cells)
            min_y = min(c * cell_size for _, c in cluster_cells)
            max_y = max((c + 1) * cell_size for _, c in cluster_cells)
            
            est_score = len(cluster_cells) * 3  # Rough estimate
            
            clusters.append({
                "bbox": {
                    "x1": min_x,
                    "y1": min_y,
                    "x2": max_x,
                    "y2": max_y
                },
                "est_score": est_score,
                "num_cells": len(cluster_cells)
            })
    
    return {
        "num_clusters": len(clusters),
        "clusters": clusters
    }