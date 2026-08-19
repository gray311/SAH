def run(ctx, args):
    import json
    
    distance_threshold = args.get("distance_threshold", 2000)
    
    # Parse program to extract fish positions
    program_text = ctx.get_program()
    mackerels = []
    sardines = []
    
    # Find fish data from input - look for coordinate patterns in the input section
    lines = program_text.split('\n')
    in_input_section = False
    for line in lines:
        if 'Input is given' in line or 'Standard Input' in line:
            in_input_section = True
            continue
        if in_input_section:
            # Try to parse coordinates - they might be in string form or as numbers
            if 'N ' in line or 'n ' in line or ('x_' in line and 'y_' not in line):
                # This might be the start of fish data
                pass
            # Look for pattern like: x_i, y_i for mackerel or sardine
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    x, y = int(parts[0]), int(parts[1])
                    # Determine if mackerel or sardine based on context
                    if 'mackerel' in line.lower() or line.count('mackerel') > 0:
                        mackerels.append((x, y))
                    else:
                        sardines.append((x, y))
                except:
                    pass
    
    # Alternative: look for direct coordinate extraction in evolve block
    # Extract all coordinate pairs from the program
    coords = []
    import re
    # Find all (x, y) patterns
    matches = re.findall(r'\(([+-]?\d+),[ ]*([+-]?\d+)\)', program_text)
    for match in matches:
        coords.append((int(match[0]), int(match[1])))
    
    # If coords found, use them
    if coords:
        # Filter to mackerels (first N points, assuming N mackerels)
        n_mackerels = len(coords) // 2
        mackerels = coords[:n_mackerels]
        sardines = coords[n_mackerels:]
    
    # If still empty, try to extract from input section more carefully
    if not mackerels or not sardines:
        # Look for fish positions in the program structure
        # The program should have parsed input somewhere
        # Try to find array-like structures
        mackerels = []
        sardines = []
        
    # Cluster mackerels by proximity
    clusters = []
    used = [False] * len(mackerels)
    
    for i, (mx, my) in enumerate(mackerels):
        if used[i]:
            continue
        
        cluster = [(mx, my)]
        used[i] = True
        
        for j, (other_x, other_y) in enumerate(mackerels):
            if j == i or used[j]:
                continue
            # Check if within distance threshold
            dist_sq = (mx - other_x)**2 + (my - other_y)**2
            if dist_sq <= distance_threshold**2:
                cluster.append((other_x, other_y))
                used[j] = True
        
        if len(cluster) >= 1:
            # Compute bounding box (MER)
            min_x = min(p[0] for p in cluster)
            max_x = max(p[0] for p in cluster)
            min_y = min(p[1] for p in cluster)
            max_y = max(p[1] for p in cluster)
            
            # Count sardines in MER
            sardines_in_mer = sum(1 for (sx, sy) in sardines if min_x <= sx <= max_x and min_y <= sy <= max_y)
            
            clusters.append({
                "mackerels": len(cluster),
                "sardines": sardines_in_mer,
                "score": len(cluster) - sardines_in_mer,
                "min_x": min_x, "max_x": max_x,
                "min_y": min_y, "max_y": max_y
            })
    
    # Sort by score (descending)
    clusters.sort(key=lambda c: c["score"], reverse=True)
    
    return {
        "num_clusters": len(clusters),
        "clusters": clusters[:20],  # Top 20 clusters
        "best_cluster": clusters[0] if clusters else None
    }