def run(ctx, args):
    vertices = args.get("vertices", [])
    if not vertices:
        return {"valid": False, "reason": "no vertices"}
    if len(vertices) < 4:
        return {"valid": False, "reason": "need >= 4 vertices, got " + str(len(vertices))}
    if len(vertices) > 1000:
        return {"valid": False, "reason": "max 1000 vertices, got " + str(len(vertices))}
    perim = 0
    for i in range(len(vertices)):
        x1, y1 = vertices[i]["x"], vertices[i]["y"]
        x2, y2 = vertices[(i+1) % len(vertices)]["x"], vertices[(i+1) % len(vertices)]["y"]
        dist = abs(x2-x1) + abs(y2-y1)
        perim += dist
        if dist == 0:
            return {"valid": False, "reason": "duplicate vertex at index " + str(i)}
        if x1 != x2 and y1 != y2:
            return {"valid": False, "reason": "non-orthogonal edge at " + str(i)}
        if not (0 <= x1 <= 100000 and 0 <= y1 <= 100000):
            return {"valid": False, "reason": "coord out of range at " + str(i)}
    if perim > 400000:
        return {"valid": False, "reason": "perimeter " + str(perim) + " > 400000"}
    return {"valid": True, "reason": "ok", "perimeter": perim, "vertex_count": len(vertices)}
