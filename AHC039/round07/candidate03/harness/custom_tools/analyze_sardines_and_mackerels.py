def run(ctx, args):
    mackerels = []
    sardines = []
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no inputs"}
    # Read mackerels (first N) and sardines (next N)
    df = ctx.read_input_df(names[0], nrows=10000)
    df['type'] = [1 if i < 5000 else -1 for i in range(len(df))]
    mackerels = df[df['type'] == 1].values.tolist()
    sardines = df[df['type'] == -1].values.tolist()
    
    # Compute mackerel bounding box
    if not mackerels:
        return {"note": "no mackerels", "bbox": [0,0,0,0], "easy_sardines": [], 
                "cluster_count": 0, "recommended_shape": "bbox"}
    mackerels_x = [p[0] for p in mackerels]
    mackerels_y = [p[1] for p in mackerels]
    min_mx, max_mx = min(mackerels_x), max(mackerels_x)
    min_my, max_my = min(mackerels_y), max(mackerels_y)
    bbox = [min_mx, min_my, max_mx, max_my]
    
    # Find sardines near bbox edges (margin = 300)
    easy_sardines = []
    margin = 300
    for s in sardines:
        sx, sy = s[0], s[1]
        if (sx < max_mx + margin or sx > min_mx - margin or
            sy < max_my + margin or sy > min_my - margin):
            easy_sardines.append(s)
    
    # Simple cluster analysis: group sardines by proximity
    clusters = []
    used = [False] * len(sardines)
    for i, s in enumerate(sardines):
        if used[i]:
            continue
        cluster = [s]
        used[i] = True
        for j in range(i+1, len(sardines)):
            if not used[j]:
                dist = ((s[0]-sardines[j][0])**2 + (s[1]-sardines[j][1])**2)**0.5
                if dist < 800:
                    cluster.append(sardines[j])
                    used[j] = True
        if len(cluster) >= 2:
            clusters.append(cluster)
    
    # Recommend shape based on analysis
    if len(easy_sardines) > len(sardines) * 0.3:
        recommended = "L-shape"
    elif len(clusters) > 3:
        recommended = "multi-rect"
    elif len(mackerels) > 3000:
        recommended = "stepped"
    else:
        recommended = "bbox"
    
    return {"bbox": bbox, "easy_sardines": easy_sardines, 
            "cluster_count": len(clusters), 
            "recommended_shape": recommended}