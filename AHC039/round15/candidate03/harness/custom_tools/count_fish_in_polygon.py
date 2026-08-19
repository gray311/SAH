def run(ctx, args):
    import json
    from collections import defaultdict
    
    polygon = args.get("polygon")
    use_kd_tree = args.get("use_kd_tree", True)
    
    if not polygon or len(polygon) < 3:
        return {"error": "invalid polygon", "mackerels": 0, "sardines": 0, "score": 1}
    
    # Build KD-tree from fish data in program
    # Parse CPP_CODE to extract fish positions
    program = ctx.get_program()
    
    fish_map = defaultdict(int)  # (x, y) -> type (+1 for mackerel, -1 for sardine)
    
    # Simple parser: look for patterns like "Point p{" or coordinate assignments
    lines = program.split('\n')
    current_x = None
    current_y = None
    is_mackerel = False
    
    in_struct = False
    for line in lines:
        line = line.strip()
        if 'struct Point' in line or 'struct Fish' in line:
            in_struct = False
            continue
        
        if '{' in line and '(' not in line.split('{')[0].split('#')[-1]:
            if 'Point' in line or 'p{' in line.lower():
                parts = line.replace('(', '').replace('{', '').split(',')
                if len(parts) >= 2:
                    try:
                        x = int(parts[0].strip())
                        y = int(parts[1].strip())
                        current_x, current_y = x, y
                    except:
                        pass
                    in_struct = True
        elif in_struct and line and not line.startswith('}'):
            if 'mackerel' in line.lower() or (current_x is not None and 'x_' in line.lower() or 'x = ' in line):
                is_mackerel = True
            elif 'sardine' in line.lower():
                is_mackerel = False
        
        if in_struct and ('}' in line or ')' in line):
            if current_x is not None:
                if is_mackerel:
                    fish_map[(current_x, current_y)] += 1
                else:
                    fish_map[(current_x, current_y)] -= 1
            in_struct = False
            current_x = None
            current_y = None
    
    # Convert polygon to list of (x, y) tuples
    poly_points = []
    for i in range(len(polygon) + 1):
        p = polygon[i % len(polygon)]
        poly_points.append((p.get("x", 0), p.get("y", 0)))
    
    # Point-in-polygon test using ray casting (axis-aligned polygon)
    def point_in_polygon(px, py, poly):
        n = len(poly)
        inside = False
        for i in range(n):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % n]
            if ((y1 > py) != (y2 > py)) and (px < (x2 - x1) * (py - y1) / (y2 - y1) + x1):
                inside = not inside
        return inside
    
    mackerels = 0
    sardines = 0
    
    for (fx, fy), fish_type in fish_map.items():
        if point_in_polygon(fx, fy, poly_points):
            if fish_type == 1:
                mackerels += 1
            else:
                sardines += 1
    
    score = mackerels - sardines + 1
    return {"mackerels": mackerels, "sardines": sardines, "score": score}
