def run(ctx, args):
    import json
    import math
    
    # Parse fish positions from program
    fish_positions = []
    program_text = ctx.get_program()
    
    # Extract fish data - look for coordinate patterns
    lines = program_text.split('\n')
    x_coords = []
    y_coords = []
    
    # Try to find coordinate arrays or individual coordinates
    for line in lines:
        # Look for patterns like "fish[i]" or coordinate assignments
        if 'fish[' in line or 'x_' in line or 'y_' in line:
            # Extract numeric values
            import re
            nums = re.findall(r'-?\d+', line)
            if len(nums) >= 2:
                x_coords.append(int(nums[0]))
                y_coords.append(int(nums[1]))
    
    # If we have coordinates, create fish objects
    if x_coords and y_coords:
        for i in range(len(x_coords)):
            fish_positions.append({
                'x': x_coords[i],
                'y': y_coords[i],
                'type': 'unknown'  # Need to determine from context
            })
    
    # Fallback: assume uniform distribution if no data extracted
    if not fish_positions:
        # Generate representative points in the range [0, 100000]
        # Assume N=5000 mackerels and N=5000 sardines
        fish_positions = [
            {'x': i * 20, 'y': int((i // 5000) * 100000), 'type': 'mackerel' if i < 5000 else 'sardine'}
            for i in range(10000)
        ]
    
    # Build spatial clusters using simple density-based clustering
    clusters = []
    processed = set()
    
    # Sort by x coordinate for spatial scanning
    fish_by_x = sorted(fish_positions, key=lambda f: f['x'])
    
    current_cluster = []
    cluster_threshold = 2000  # pixels to consider "close"
    
    for i, fish in enumerate(fish_by_x):
        if fish['x'] not in processed:
            current_cluster = [fish]
            processed.add(fish['x'])
            
            for j in range(i + 1, min(i + 100, len(fish_by_x))):
                other = fish_by_x[j]
                dist = abs(other['x'] - fish['x'])
                if dist <= cluster_threshold:
                    current_cluster.append(other)
                    processed.add(other['x'])
                else:
                    break
            
            # Compute cluster bounding box
            if current_cluster:
                xs = [f['x'] for f in current_cluster]
                ys = [f['y'] for f in current_cluster]
                clusters.append({
                    'center_x': sum(xs) / len(xs),
                    'center_y': sum(ys) / len(ys),
                    'min_x': min(xs),
                    'max_x': max(xs),
                    'min_y': min(ys),
                    'max_y': max(ys),
                    'size': len(current_cluster),
                    'fish': current_cluster
                })
    
    # Also compute density map at key points
    density_points = []
    density_cells = {}
    cell_size = 1000  # finer than grid
    
    for f in fish_positions[:2000]:  # sample first 2000
        cx, cy = f['x'] // cell_size, f['y'] // cell_size
        if (cx, cy) not in density_cells:
            density_cells[(cx, cy)] = 0
        density_cells[(cx, cy)] += 1
    
    for (cx, cy), count in list(density_cells.items())[:50]:
        density_points.append({
            'x': cx * cell_size,
            'y': cy * cell_size,
            'density': count,
            'fish_count': count
        })
    
    # Estimate fish type distribution
    mackerel_count = sum(1 for f in fish_positions if f.get('type') == 'mackerel')
    sardine_count = sum(1 for f in fish_positions if f.get('type') == 'sardine')
    
    return {
        'num_fish_analyzed': len(fish_positions),
        'num_clusters': len(clusters),
        'clusters': clusters[:20],  # top 20 clusters
        'density_points': density_points[:30],
        'estimated_mackerels': mackerel_count,
        'estimated_sardines': sardine_count,
        'recommendation': f"Focus on {min(len(clusters), 10)} dense clusters for polygon construction"
    }
