def run(ctx, args):
    poly = args.get("polygon", [])
    grid_res = args.get("grid_resolution", 500)
    sample_rate = args.get("sample_rate", 100)
    
    # Validate polygon constraints
    if len(poly) < 4 or len(poly) > 1000:
        return {"valid": False, "note": "Polygon must have 4-1000 vertices"}
    
    # Check perimeter
    perimeter = 0
    for i in range(len(poly)):
        p1 = poly[i]
        p2 = poly[(i+1) % len(poly)]
        perimeter += abs(p1["x"] - p2["x"]) + abs(p1["y"] - p2["y"])
    
    if perimeter > 400000:
        return {"valid": False, "perimeter": perimeter, "note": "Perimeter exceeds 400000"}
    
    # Get bounds
    min_x = min(p["x"] for p in poly) if poly else 0
    max_x = max(p["x"] for p in poly) if poly else 100000
    min_y = min(p["y"] for p in poly) if poly else 0
    max_y = max(p["y"] for p in poly) if poly else 100000
    
    # Check coordinate bounds
    for p in poly:
        if not (0 <= p["x"] <= 100000 and 0 <= p["y"] <= 100000):
            return {"valid": False, "note": "Coordinates out of bounds"}
    
    # Estimate score using grid approximation
    # Assume uniform density: 5000 mackerels and 5000 sardines in 100000x100000 area
    # = 0.5 fish per 1000000 sq units = 0.0000005 per sq unit
    total_area = 100000 * 100000  # 1e10
    fish_per_area = 10000 / total_area  # 1e-6 per sq unit
    
    polygon_area = (max_x - min_x) * (max_y - min_y)
    est_total = polygon_area * fish_per_area
    est_mackerels = int(est_total * 0.5)  # Assume 50% mackerels
    est_sardines = int(est_total * 0.5)   # Assume 50% sardines
    
    score = max(0, est_mackerels - est_sardines + 1)
    
    return {
        "valid": True,
        "perimeter": perimeter,
        "bounds": {"min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y},
        "area": polygon_area,
        "estimated_mackerels": est_mackerels,
        "estimated_sardines": est_sardines,
        "estimated_score": score,
        "note": "Grid-based estimate: not exact, use for ranking candidates"
    }
