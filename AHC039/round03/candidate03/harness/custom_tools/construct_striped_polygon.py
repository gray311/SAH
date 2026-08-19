def run(ctx, args):
    stripes = args.get("stripes", [])
    if not stripes:
        return {"note": "no stripes", "vertices": [(0, 0), (1, 0), (1, 1), (0, 1)]}
    all_x = []
    all_y = []
    for s in stripes:
        all_x.extend([s["x1"], s["x2"]])
        all_y.extend([s["y1"], s["y2"]])
    if not all_x:
        return {"note": "no valid stripes", "vertices": [(0, 0), (1, 0), (1, 1), (0, 1)]}
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    perimeter = 2 * (max_x - min_x + max_y - min_y)
    if perimeter > 400000:
        return {"note": "union perimeter exceeds limit", "vertices": []}
    vertices = [
        (min_x, min_y),
        (max_x, min_y),
        (max_x, max_y),
        (min_x, max_y)
    ]
    return {"vertices": vertices, "num_stripes": len(stripes), "perimeter": perimeter}
