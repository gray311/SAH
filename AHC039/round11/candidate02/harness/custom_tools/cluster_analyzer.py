def run(ctx, args):
    import json, math
    
    input_names = ctx.list_task_inputs()
    if not input_names:
        return {"clusters": []}
    
    try:
        mackerel_text = ctx.read_input_sample(input_names[0], nrows=15000)
        coords = []
        for line in mackerel_text.split('\n')[:5000]:
            line = line.strip()
            if line:
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        coords.append((int(parts[0]), int(parts[1])))
                    except:
                        pass
        mackerels = coords[:5000]
    except:
        return {"clusters": []}
    
    if not mackerels:
        return {"clusters": []}
    
    clusters = []
    threshold = 10000.0
    
    for mack in mackerels:
        assigned = False
        for cluster in clusters:
            min_dist = float('inf')
            for cx, cy in cluster['points']:
                dist = math.sqrt((mack[0] - cx)**2 + (mack[1] - cy)**2)
                if dist < min_dist:
                    min_dist = dist
            if min_dist <= threshold:
                cluster['points'].append(mack)
                cluster['mackerel_count'] += 1
                assigned = True
                break
        if not assigned:
            clusters.append({
                'points': [mack],
                'mackerel_count': 1,
                'sardine_count': 0,
                'min_x': mack[0], 'max_x': mack[0],
                'min_y': mack[1], 'max_y': mack[1],
                'net_score': 1
            })
    
    sardine_coords = []
    if len(input_names) > 1:
        try:
            sardine_text = ctx.read_input_sample(input_names[1], nrows=15000)
            for line in sardine_text.split('\n')[:5000]:
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            sardine_coords.append((int(parts[0]), int(parts[1])))
                        except:
                            pass
        except:
            pass
    
    for cluster in clusters:
        min_x = min(p[0] for p in cluster['points'])
        max_x = max(p[0] for p in cluster['points'])
        min_y = min(p[1] for p in cluster['points'])
        max_y = max(p[1] for p in cluster['points'])
        cluster['min_x'], cluster['max_x'], cluster['min_y'], cluster['max_y'] = min_x, max_x, min_y, max_y
        
        if sardine_coords:
            cluster['sardine_count'] = sum(1 for sx, sy in sardine_coords if cluster['min_x'] <= sx <= cluster['max_x'] and cluster['min_y'] <= sy <= cluster['max_y'])
        cluster['net_score'] = cluster['mackerel_count'] - cluster['sardine_count'] + 1
    
    clusters.sort(key=lambda c: c['net_score'], reverse=True)
    return {"clusters": clusters[:20]}