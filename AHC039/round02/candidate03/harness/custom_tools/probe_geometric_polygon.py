def run(ctx, args):
    """Lightweight probe for orthogonal polygon construction."""
    names = ctx.list_task_inputs()
    if not names:
        return {"approx_score": 0.0, "note": "no inputs"}
    
    mackerels = []
    sardines = []
    
    for name in names:
        try:
            df = ctx.read_input_df(name, nrows=1000)
            for _, row in df.iterrows():
                mackerels.append((int(row['x']), int(row['y'])))
                sardines.append((int(row['x']), int(row['y'])))
        except:
            pass
    
    if len(mackerels) < 100 or len(sardines) < 100:
        return {"approx_score": 0.5, "note": "insufficient data"}
    
    # Simple bounding box polygon
    min_x = min(p[0] for p in mackerels)
    max_x = max(p[0] for p in mackerels)
    min_y = min(p[1] for p in mackerels)
    max_y = max(p[1] for p in mackerels)
    
    # Count points in bounding box
    m_count = 0
    s_count = 0
    for p in mackerels:
        if min_x <= p[0] <= max_x and min_y <= p[1] <= max_y:
            m_count += 1
    for p in sardines:
        if min_x <= p[0] <= max_x and min_y <= p[1] <= max_y:
            s_count += 1
    
    score = max(0.0, m_count - s_count + 1)
    
    return {"approx_score": float(score),
            "policy": "bounding_box",
            "m_count": m_count,
            "s_count": s_count,
            "bbox": [min_x, min_y, max_x, max_y]}
