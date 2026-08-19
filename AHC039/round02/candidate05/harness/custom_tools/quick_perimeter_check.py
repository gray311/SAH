def run(ctx, args):
    vertices = args.get("vertices", [])
    perim = 0
    for i in range(len(vertices)):
        x1, y1 = vertices[i]["x"], vertices[i]["y"]
        x2, y2 = vertices[(i+1) % len(vertices)]["x"], vertices[(i+1) % len(vertices)]["y"]
        perim += abs(x2 - x1) + abs(y2 - y1)
    status = "ok" if perim <= 400000 else "over_budget"
    return {"perimeter": perim, "status": status}
