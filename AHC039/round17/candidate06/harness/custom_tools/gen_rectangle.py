def run(ctx, args):
    import random
    seed_x = args.get("seed_x", 50000)
    seed_y = args.get("seed_y", 50000)
    expansion = args.get("expansion", 200)
    
    # Clamp to valid range
    left = max(0, seed_x - expansion)
    right = min(100001, seed_x + expansion + 1)
    bottom = max(0, seed_y - expansion)
    top = min(100001, seed_y + expansion + 1)
    
    # Ensure minimum size for valid polygon
    if right - left < 1: right = left + 1
    if top - bottom < 1: top = bottom + 1
    
    perimeter = 2 * ((right - left) + (top - bottom))
    if perimeter > 400000:
        # Scale down if too large
        scale = 400000 / perimeter
        left = max(0, left * scale)
        right = min(100001, right * scale)
        bottom = max(0, bottom * scale)
        top = min(100001, top * scale)
    
    vertices = [
        {"x": int(left), "y": int(bottom)},
        {"x": int(right), "y": int(bottom)},
        {"x": int(right), "y": int(top)},
        {"x": int(left), "y": int(top)}
    ]
    
    return {"vertices": vertices, "perimeter": perimeter, "type": "rectangle"}
