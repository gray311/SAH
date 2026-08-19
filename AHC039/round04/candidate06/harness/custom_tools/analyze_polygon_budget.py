def run(ctx, args):
    vertices = args.get("vertices", [])
    if not vertices or len(vertices) < 4:
        return {"error": "need at least 4 vertices", "valid": False}
    
    m = len(vertices)
    if m > 1000:
        return {"error": f"vertices {m} > 1000", "valid": False}
    
    perimeter = 0
    for i in range(m):
        p1 = vertices[i]
        p2 = vertices[(i+1) % m]
        perimeter += abs(p1["x"] - p2["x"]) + abs(p1["y"] - p2["y"])
    
    valid = perimeter <= 400000
    result = {
        "vertices": m,
        "perimeter": perimeter,
        "valid_constraints": valid,
        "error": None if valid else f"perimeter {perimeter} > 400,000 or vertices > 1000"
    }
    return result