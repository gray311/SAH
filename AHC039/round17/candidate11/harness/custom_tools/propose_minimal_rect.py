def run(ctx, args):
    p1 = args.get("p1")
    p2 = args.get("p2")
    padding = args.get("padding", 150)
    
    if p1 is None or p2 is None:
        return {"valid": False, "error": "missing points"}
    
    x1, y1 = p1["x"], p1["y"]
    x2, y2 = p2["x"], p2["y"]
    
    min_x = min(x1, x2) - padding
    max_x = max(x1, x2) + padding
    min_y = min(y1, y2) - padding
    max_y = max(y1, y2) + padding
    
    # Clamp to bounds
    min_x = max(0, min_x)
    max_x = min(100000, max_x)
    min_y = max(0, min_y)
    max_y = min(100000, max_y)
    
    if min_x >= max_x or min_y >= max_y:
        return {"valid": False, "error": "invalid rectangle"}
    
    w = max_x - min_x
    h = max_y - min_y
    perimeter = 2 * (w + h)
    
    if perimeter > 400000:
        return {"valid": False, "error": "perimeter exceeds limit"}
    
    return {
        "valid": True,
        "vertices": [
            (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)
        ],
        "perimeter": int(perimeter),
        "width": w,
        "height": h
    }