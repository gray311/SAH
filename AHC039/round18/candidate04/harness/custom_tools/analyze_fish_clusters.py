def run(ctx, args):
    program_text = ctx.get_program()
    mackerels = []
    sardines = []
    
    # Parse fish coordinates from the C++ code
    lines = program_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('fish['):
            try:
                content = line.replace('fish[', '').replace(']', '').strip()
                parts = content.split(',')
                if len(parts) >= 2:
                    coords = []
                    for p in parts:
                        p = p.strip()
                        if p:
                            coords.append(int(p))
                    if len(coords) >= 2:
                        x, y = coords[0], coords[1]
                        ftype = 1 if 'mackerel' in line.lower() else -1
                        mackerels.append((x, y)) if ftype == 1 else sardines.append((x, y))
            except:
                pass
        i += 1
    
    if not mackerels:
        return {"note": "no mackerels found"}
    
    # Cluster mackerels within 500-unit radius using simple distance grouping
    clusters = []
    used = [False] * len(mackerels)
    for m_idx in range(len(mackerels)):
        if used[m_idx]:
            continue
        cluster = [mackerels[m_idx]]
        used[m_idx] = True
        
        for other_idx in range(m_idx + 1, len(mackerels)):
            if not used[other_idx]:
                p1 = mackerels[m_idx]
                p2 = mackerels[other_idx]
                dist_sq = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
                if dist_sq <= 250000:  # 500^2
                    cluster.append(mackerels[other_idx])
                    used[other_idx] = True
        
        if len(cluster) >= 2:
            xs = [p[0] for p in cluster]
            ys = [p[1] for p in cluster]
            clusters.append({
                "center": [(sum(xs)/len(xs), sum(ys)/len(ys))],
                "min_x": min(xs), "min_y": min(ys),
                "max_x": max(xs), "max_y": max(ys),
                "size": len(cluster)
            })
    
    # For clusters with fewer than 2 mackerels, add individually
    for m_idx in range(len(mackerels)):
        if not used[m_idx]:
            m = mackerels[m_idx]
            xs, ys = [m[0]], [m[1]]
            clusters.append({
                "center": [m],
                "min_x": m[0], "min_y": m[1],
                "max_x": m[0], "max_y": m[1],
                "size": 1
            })
    
    # Suggest vertex positions for each cluster
    vertices_suggestions = []
    for c in clusters:
        cx, cy = c["min_x"], c["min_y"]
        dx, dy = c["max_x"] - c["min_x"], c["max_y"] - c["min_y"]
        
        # Suggest vertices at cluster boundaries with small padding
        vx1, vy1 = c["min_x"] - 50, c["min_y"]
        vx2, vy2 = c["max_x"] + 50, c["min_y"]
        vx3, vy3 = c["max_x"] + 50, c["max_y"] + 50
        vx4, vy4 = c["min_x"] - 50, c["max_y"] + 50
        
        vertices_suggestions.append({
            "cluster_idx": len(vertices_suggestions),
            "vertices": [
                {"x": max(0, min(100000, vx1)), "y": max(0, min(100000, vy1))},
                {"x": max(0, min(100000, vx2)), "y": max(0, min(100000, vy2))},
                {"x": max(0, min(100000, vx3)), "y": max(0, min(100000, vy3))},
                {"x": max(0, min(100000, vx4)), "y": max(0, min(100000, vy4))}
            ],
            "size": c["size"]
        })
    
    return {
        "num_clusters": len(clusters),
        "total_mackerels": len(mackerels),
        "num_sardines": len(sardines),
        "clusters": clusters,
        "vertices_suggestions": vertices_suggestions
    }
