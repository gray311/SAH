def run(ctx, args):
    dist_thresh = args.get("distance_threshold", 2000)
    max_clusters = args.get("num_clusters", -1)
    
    program = ctx.get_program()
    mackerels = []
    sardines = []
    
    for line in program.split('\n'):
        line = line.strip()
        if not line or line.startswith('//'):
            continue
        parts = line.split()
        if len(parts) >= 2:
            try:
                x = int(parts[0])
                y = int(parts[1])
                if 'mackerel' in line.lower():
                    mackerels.append((x, y))
                elif 'sardine' in line.lower():
                    sardines.append((x, y))
            except:
                pass
    
    # Cluster mackerels using BFS
    from collections import deque
    clusters = []
    visited = set()
    
    for i, (mx, my) in enumerate(mackerels):
        if i in visited:
            continue
        
        cluster_points = []
        queue = deque([i])
        visited.add(i)
        
        while queue:
            j = queue.popleft()
            cluster_points.append(mackerels[j])
            xj, yj = mackerels[j]
            
            for k, (xk, yk) in enumerate(mackerels):
                if k in visited:
                    continue
                dist = abs(xj - xk) + abs(yj - yk)
                if dist <= dist_thresh:
                    visited.add(k)
                    queue.append(k)
        
        if cluster_points:
            min_x = min(p[0] for p in cluster_points)
            max_x = max(p[0] for p in cluster_points)
            min_y = min(p[1] for p in cluster_points)
            max_y = max(p[1] for p in cluster_points)
            
            # Count sardines inside
            s_count = 0
            for sx, sy in sardines:
                if min_x <= sx <= max_x and min_y <= sy <= max_y:
                    s_count += 1
            
            m_count = len(cluster_points)
            score = m_count - s_count
            clusters.append({
                'bbox': (min_x, max_x, min_y, max_y),
                'm': m_count,
                's': s_count,
                'score': score
            })
    
    if max_clusters > 0 and len(clusters) > max_clusters:
        clusters.sort(key=lambda c: c['score'], reverse=True)
        clusters = clusters[:max_clusters]
    
    return {
        'clusters': clusters,
        'num_clusters': len(clusters),
        'note': f'Found {len(clusters)} clusters from {len(mackerels)} mackerels'
    }
