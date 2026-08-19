def run(ctx, args):
    x_min = args.get("x_min", 0)
    x_max = args.get("x_max", 100000)
    y_min = args.get("y_min", 0)
    y_max = args.get("y_max", 100000)
    x_min = max(0, x_min)
    x_max = min(100000, x_max)
    y_min = max(0, y_min)
    y_max = min(100000, y_max)
    if x_min >= x_max or y_min >= y_max:
        return {"error": "invalid rectangle", "vertices": []}
    perimeter = 2 * (x_max - x_min + y_max - y_min)
    if perimeter > 400000:
        return {"note": "perimeter exceeds limit", "vertices": []}
    vertices = [
        (x_min, y_min),
        (x_max, y_min),
        (x_max, y_max),
        (x_min, y_max)
    ]
    return {"vertices": vertices, "perimeter": perimeter, "area": (x_max - x_min) * (y_max - y_min)}