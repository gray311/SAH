def run(ctx, args):
    threshold = args.get("cluster_threshold", 5000)
    max_boxes = args.get("max_boxes", 20)
    
    # Parse fish positions from program
    program = ctx.get_program()
    mackerels = []
    sardines = []
    
    for line in program.split('\n'):
        # Look for mackerel positions: fish[i] is mackerel at (x, y)
        if 'mackerel' in line.lower():
            parts = line.replace('mackerel', '').replace('(', '').replace(')', '').strip().split(',')
            if len(parts) >= 2:
                try:
                    mackerels.append((int(parts[0]), int(parts[1])))
                except:
                    pass
        elif 'sardine' in line.lower():
            parts = line.replace('sardine', '').replace('(', '').replace(')', '').strip().split(',')
            if len(parts) >= 2:
                try:
                    sardines.append((int(parts[0]), int(parts[1])))
                except:
                    pass
    
    # Build KD-tree for sardines (for fast counting)
    # Simple approach: create bounding box and count points
    def bbox_contains_point(pts, min_x, max_x, min_y, max_y):
        if not pts:
            return 0
        count = 0
        for px, py in pts:
            if min_x <= px <= max_x and min_y <= py <= max_y:
                count += 1
        return count
    
    # Find clusters using simple spatial grouping
    clusters = []
    visited = set()
    
    if len(mackerels) > 0:
        for i, (mx, my) in enumerate(mackerels):
            if i in visited:
                continue
            
            cluster = [(mx, my)]
            visited.add(i)
            
            # Find all mackerels within threshold
            changed = True
            while changed:
                changed = False
                for j, (mj, mjy) in enumerate(mackerels):
                    if j in visited:
                        continue
                    
                    # Check if within threshold (use Manhattan distance for speed)
                    dist = abs(mx - mj) + abs(my - mjy)
                    if dist <= threshold:
                        cluster.append((mj, mjy))
                        visited.add(j)
                        changed = True
            
            # Compute bounding box
            xs = [p[0] for p in cluster]
            ys = [p[1] for p in cluster]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            
            # Count sardines in this box
            s_count = bbox_contains_point(sardines, min_x, max_x, min_y, max_y)
            m_count = len(cluster)
            
            clusters.append({
                'min_x': min_x, 'max_x': max_x,
                'min_y': min_y, 'max_y': max_y,
                'mackerels': m_count, 'sardines': s_count,
                'score': m_count - s_count
            })
    
    # Combine adjacent clusters if beneficial
    combined_candidates = []
    simple_candidates = []
    
    for c in clusters[:max_boxes]:
        # Ensure valid rectangle
        if c['max_x'] < c['min_x'] or c['max_y'] < c['min_y']:
            continue
        
        simple_candidates.append({
            'vertices': [
                (c['min_x'], c['min_y']),
                (c['max_x'], c['min_y']),
                (c['max_x'], c['max_y']),
                (c['min_x'], c['max_y'])
            ],
            'score': c['score'],
            'mackerels': c['mackerels'],
            'sardines': c['sardines']
        })
        
        # Try rotated version
        simple_candidates.append({
            'vertices': [
                (c['min_x'], c['max_y']),
                (c['max_x'], c['max_y']),
                (c['max_x'], c['min_y']),
                (c['min_x'], c['min_y'])
            ],
            'score': c['score'],
            'mackerels': c['mackerels'],
            'sardines': c['sardines']
        })
    
    # Also try combining top few clusters
    if len(clusters) >= 4:
        combined = clusters[:4]
        all_xs = [c['min_x'] for c in combined] + [c['max_x'] for c in combined]
        all_ys = [c['min_y'] for c in combined] + [c['max_y'] for c in combined]
        min_all_x, max_all_x = min(all_xs), max(all_xs)
        min_all_y, max_all_y = min(all_ys), max(all_ys)
        
        # Count total mackerels and sardines in combined region
        # (simplified: might double-count, but gives approximate score)
        combined_candidates.append({
            'vertices': [
                (min_all_x, min_all_y),
                (max_all_x, min_all_y),
                (max_all_x, max_all_y),
                (min_all_x, max_all_y)
            ],
            'score': sum(c['score'] for c in combined),
            'mackerels': sum(c['mackerels'] for c in combined),
            'sardines': 0  # Approximate
        })
    
    return {
        'clusters': clusters,
        'simple_candidates': simple_candidates,
        'combined_candidates': combined_candidates,
        'total_mackerels_found': len(mackerels),
        'total_sardines_found': len(sardines)
    }
