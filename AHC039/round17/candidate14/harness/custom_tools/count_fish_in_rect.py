def run(ctx, args):
    mackerels = args.get("mackerels", {})
    sardines = args.get("sardines", {})
    min_x = args.get("min_x")
    max_x = args.get("max_x")
    min_y = args.get("min_y")
    max_y = args.get("max_y")
    
    if any(v is None for v in [min_x, max_x, min_y, max_y]):
        return {"error": "missing rectangle bounds"}
    
    m_coords = mackerels.get("coords", [])
    s_coords = sardines.get("coords", [])
    
    m_count = 0
    s_count = 0
    
    for x, y in m_coords:
        if min_x <= x <= max_x and min_y <= y <= max_y:
            m_count += 1
    
    for x, y in s_coords:
        if min_x <= x <= max_x and min_y <= y <= max_y:
            s_count += 1
    
    return {
        "mackerels": m_count,
        "sardines": s_count,
        "score": max(0, m_count - s_count + 1)
    }
