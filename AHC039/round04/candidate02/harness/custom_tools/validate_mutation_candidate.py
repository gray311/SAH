def run(ctx, args):
    import math
    vertices = args.get("polygon_vertices", [])
    
    if len(vertices) < 4:
        return {"valid": False, "reason": "polygon needs at least 4 vertices"}
    if len(vertices) > 1000:
        return {"valid": False, "reason": "too many vertices, max 1000"}
    
    # Check axis alignment and perimeter
    perimeter = 0
    axis_aligned = True
    coords_valid = True
    prev_x = None
    prev_y = None
    
    for i, v in enumerate(vertices):
        cur_x, cur_y = v.get("x", 0), v.get("y", 0)
        
        # Coordinate range check
        if not (0 <= cur_x <= 100000 and 0 <= cur_y <= 100000):
            coords_valid = False
        
        # Axis alignment: consecutive vertices must share x or y
        if prev_x is not None:
            if cur_x != prev_x and cur_y != prev_y:
                axis_aligned = False
            # Perimeter contribution
            perimeter += abs(cur_x - prev_x) + abs(cur_y - prev_y)
        
        prev_x, prev_y = cur_x, cur_y
    
    if not coords_valid:
        return {"valid": False, "reason": "coordinates outside [0, 100000]^2"}
    if not axis_aligned:
        return {"valid": False, "reason": "some edges not axis-aligned"}
    if perimeter > 400000:
        return {"valid": False, "reason": f"perimeter {perimeter} exceeds 400000"}
    
    # Check distinct vertices
    seen = set()
    for v in vertices:
        pt = (v.get("x", 0), v.get("y", 0))
        if pt in seen:
            return {"valid": False, "reason": "duplicate vertex"}
        seen.add(pt)
    
    return {"valid": True, "perimeter": perimeter, "vertices_count": len(vertices)}
