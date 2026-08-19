def run(ctx, args):
    import json
    from collections import defaultdict
    
    # Parse fish positions from the C++ program's input section
    program_text = ctx.get_program()
    fish_by_pos = defaultdict(int)
    fish_types = {}  # pos -> type
    
    # Find the input data in the program (it contains all fish coordinates)
    # The program reads from stdin, so we need to extract from global data
    # Look for patterns like mackerels[...], sardines[...] or raw coordinates
    
    # Alternative: the program structure shows fish coordinates in arrays
    # Extract all coordinate pairs
    import re
    coords = re.findall(r'\[\s*(\d+)\s*,\s*(\d+)\s*\]', program_text)
    
    mackerels = []
    sardines = []
    
    for i, (x, y) in enumerate(coords):
        if i < 5000:  # First 5000 are mackerels (N=5000)
            mackerels.append((int(x), int(y)))
        else:  # Next 5000 are sardines
            sardines.append((int(x), int(y)))
    
    # Build hash map for O(1) lookup
    all_fish = {}
    for x, y in mackerels:
        key = (x, y)
        all_fish[key] = 1  # mackerel
    for x, y in sardines:
        key = (x, y)
        all_fish[key] = -1  # sardine
    
    # Find mackerel clusters using local density
    # A cluster is a group of mackerels within distance 500
    clusters = []
    visited = set()
    
    for i, (mx, my) in enumerate(mackerels):
        if (mx, my) in visited:
            continue
        
        cluster = []
        queue = [(mx, my)]
        while queue:
            cx, cy = queue.pop(0)
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            cluster.append((cx, cy))
            
            # Add nearby mackerels
            for j, (nx, ny) in enumerate(mackerels):
                if (nx, ny) in visited:
                    continue
                dist = abs(nx - cx) + abs(ny - cy)  # Manhattan
                if dist <= 800:  # Cluster radius
                    queue.append((nx, ny))
        
        if len(cluster) >= 2:  # Only meaningful clusters
            # Compute cluster center and bounding box
            min_x = min(p[0] for p in cluster)
            max_x = max(p[0] for p in cluster)
            min_y = min(p[1] for p in cluster)
            max_y = max(p[1] for p in cluster)
            center_x = (min_x + max_x) // 2
            center_y = (min_y + max_y) // 2
            
            # Count sardines in cluster bounding box
            sardine_count = 0
            for sx, sy in sardines:
                if min_x <= sx <= max_x and min_y <= sy <= max_y:
                    sardine_count += 1
            
            clusters.append({
                "center": (center_x, center_y),
                "min_x": min_x, "max_x": max_x,
                "min_y": min_y, "max_y": max_y,
                "mackerel_count": len(cluster),
                "sardine_count": sardine_count,
                "density": len(cluster) / max((max_x - min_x + 1) * (max_y - min_y + 1), 1)
            })
    
    # Sort clusters by mackerel density
    clusters.sort(key=lambda c: c["mackerel_count"] / max((c["max_x"] - c["min_x"] + 1) * (c["max_y"] - c["min_y"] + 1), 1), reverse=True)
    
    # Return top clusters
    return {
        "num_mackerels": len(mackerels),
        "num_sardines": len(sardines),
        "top_clusters": clusters[:10],
        "all_clusters": clusters
    }
