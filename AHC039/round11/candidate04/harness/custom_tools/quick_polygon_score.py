def run(ctx, args):
    vertices = args.get("vertices", [])
    if len(vertices) < 4:
        return {"error": "need at least 4 vertices", "score": 0}
    
    perimeter = 0
    for i in range(len(vertices)):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % len(vertices)]
        perimeter += abs(p1["x"] - p2["x"]) + abs(p1["y"] - p2["y"])
    
    if perimeter > 400000:
        return {"error": "perimeter exceeds limit", "score": 0, "mackerels": 0, "sardines": 0}
    
    program_text = ctx.get_program()
    all_coords = []
    
    for line in program_text.split('\n'):
        coords = re.findall(r'(\d+)\s*(x|X)', line)
        coords_y = re.findall(r'(\d+)\s*(y|Y)', line)
        if coords and coords_y:
            for i in range(min(len(coords), len(coords_y))):
                all_coords.append((int(coords[i][0]), int(coords_y[i][0])))
    
    mackerels = all_coords[:5000]
    sardines = all_coords[5000:10000]
    mackerels = [(x, y) for (x, y) in mackerels if 0 <= x <= 100000 and 0 <= y <= 100000]
    sardines = [(x, y) for (x, y) in sardines if 0 <= x <= 100000 and 0 <= y <= 100000]
    
    m_count = 0
    s_count = 0
    
    for mx, my in mackerels:
        if point_in_polygon((mx, my), vertices):
            m_count += 1
    
    for sx, sy in sardines:
        if point_in_polygon((sx, sy), vertices):
            s_count += 1
    
    score = max(0, m_count - s_count + 1)
    
    return {"mackerels": m_count, "sardines": s_count, "score": score, "perimeter": perimeter}

def point_in_polygon(pt, vertices):
    x, y = pt
    n = len(vertices)
    inside = False
    j = n - 1
    for i in range(n):
        vi = vertices[i]
        vj = vertices[j]
        if ((vi["y"] > y) != (vj["y"] > y)):
            xi = vi["x"] - (vi["y"] - vj["y"]) * (vi["x"] - vj["x"]) / (vi["y"] - vj["y"])
            if x < xi:
                inside = not inside
        j = i
    return inside
