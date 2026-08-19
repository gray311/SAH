def run(ctx, args):
    rectangles = args.get("rectangles", [])
    
    # Validate constraints
    total_perimeter = 0
    total_vertices = 0
    total_mackerels = 0
    total_sardines = 0
    
    # Read fish positions
    lines = ctx.read_input_sample("input.txt", nrows=10001)
    lines = lines.strip().split('\n')
    
    mackerels = []
    sardines = []
    
    for i, line in enumerate(lines[1:5001]):
        if not line.strip():
            continue
        try:
            coords = list(map(int, line.strip().split(',')))
        except ValueError:
            continue
        if len(coords) == 2:
            mackerels.append((coords[0], coords[1]))
    
    for i in range(5000):
        lines_5000 = lines[5001 + i] if 5001 + i < len(lines) else ""
        if not lines_5000.strip():
            continue
        try:
            coords = list(map(int, lines_5000.strip().split(',')))
        except ValueError:
            continue
        if len(coords) == 2:
            sardines.append((coords[0], coords[1]))
    
    for r in rectangles:
        x1, y1 = r["x1"], r["y1"]
        x2, y2 = r["x2"], r["y2"]
        dx = x2 - x1 + 1
        dy = y2 - y1 + 1
        
        perimeter = 2 * (dx + dy)
        total_perimeter += perimeter
        total_vertices += 4
        
        # Count mackerels and sardines in this rectangle
        for mx, my in mackerels:
            if x1 <= mx <= x2 and y1 <= my <= y2:
                total_mackerels += 1
        
        for sx, sy in sardines:
            if x1 <= sx <= x2 and y1 <= sy <= y2:
                total_sardines += 1
    
    valid = total_perimeter <= 400000 and total_vertices <= 1000
    
    per_rectangle = []
    total_score = 0
    
    for r in rectangles:
        x1, y1 = r["x1"], r["y1"]
        x2, y2 = r["x2"], r["y2"]
        
        m_count = sum(1 for mx, my in mackerels if x1 <= mx <= x2 and y1 <= my <= y2)
        s_count = sum(1 for sx, sy in sardines if x1 <= sx <= x2 and y1 <= sy <= y2)
        rect_score = max(0, m_count - s_count + 1)
        total_score += rect_score
        
        per_rectangle.append({
            "rect": f"{r['x1']},{r['y1']},{r['x2']},{r['y2']}",
            "mackerels": m_count,
            "sardines": s_count,
            "score": rect_score
        })
    
    return {
        "valid": valid,
        "total_score": total_score,
        "per_rectangle": per_rectangle,
        "perimeter": total_perimeter,
        "total_vertices": total_vertices,
        "mackerels": total_mackerels,
        "sardines": total_sardines
    }