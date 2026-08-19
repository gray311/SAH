def run(ctx, args):
    vertices = args.get("vertices", [])
    if not isinstance(vertices, list) or len(vertices) < 4:
        return {"score": 0, "error": "Invalid polygon: need at least 4 vertices"}
    
    poly = []
    for v in vertices:
        if isinstance(v, dict) and "x" in v and "y" in v:
            poly.append((v["x"], v["y"]))
        else:
            return {"score": 0, "error": "Invalid vertex format"}
    
    if len(poly) < 4:
        return {"score": 0, "error": "Need at least 4 vertices"}
    
    # Point-in-polygon using ray casting
    def point_in_polygon(point, polygon):
        x, y = point
        inside = False
        n = len(polygon)
        j = n - 1
        for i in range(n):
            xi, yi = polygon[i]
            xj, yj = polygon[j]
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-10) + xi):
                inside = not inside
            j = i
        return inside
    
    # Read fish from task inputs
    fish_data = []  # (x, y)
    names = ctx.list_task_inputs()
    
    for name in names:
        try:
            content = ctx.read_input_sample(name, nrows=10001)
            if content:
                lines = content.strip().split('\n')
                if len(lines) > 1:
                    for line in lines:
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            fx, fy = int(parts[0]), int(parts[1])
                            fish_data.append((fx, fy))
        except:
            continue
    
    # Fish types: first N from input are mackerels (1), next N are sardines (-1)
    # But we only have coordinates in the input file - we need N from context or estimate
    # Use N=5000 (fixed per task description)
    N = 5000
    mackerels = 0
    sardines = 0
    
    # Process fish in pairs (x_i, y_i) for i=0..2N-1
    idx = 0
    for i in range(2 * N):
        if idx < len(fish_data):
            fx, fy = fish_data[idx]
            if point_in_polygon((fx, fy), poly):
                if i < N:  # First N are mackerels
                    mackerels += 1
                else:  # Next N are sardines
                    sardines += 1
            idx += 1
    
    score = max(0, mackerels - sardines + 1)
    return {"score": score, "mackerels": mackerels, "sardines": sardines}
