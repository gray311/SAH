def run(ctx, args):
    import random
    max_candidates = args.get("max_candidates", 50)
    
    program = ctx.get_program()
    fish_data = []
    for line in program.split('\n'):
        line = line.strip()
        if 'mackerel' in line.lower() or 'sardine' in line.lower():
            if '[' in line and ']' in line:
                try:
                    coords = line.split('[')[1].split(']')[0].split(',')
                    if len(coords) >= 2:
                        x, y = int(coords[0]), int(coords[1])
                        fish_type = 1 if 'mackerel' in line.lower() else -1
                        fish_data.append((x, y, fish_type))
                except:
                    continue
    
    if not fish_data:
        return {"error": "No fish data found"}
    
    x_coords = sorted(set(p[0] for p in fish_data))
    y_coords = sorted(set(p[1] for p in fish_data))
    
    # Add boundary points
    x_coords = sorted(set(x_coords + [0, 100000]))
    y_coords = sorted(set(y_coords + [0, 100000]))
    
    candidates = []
    
    # Enumerate rectangles from coordinate grid
    for xi in range(len(x_coords)-1):
        for yi in range(len(y_coords)-1):
            x1, x2 = x_coords[xi], x_coords[xi+1]
            y1, y2 = y_coords[yi], y_coords[yi+1]
            if x2 - x1 > 10000 or y2 - y1 > 10000:  # Skip too large
                continue
            candidates.append({"type": "rect", "x1": x1, "y1": y1, "x2": x2, "y2": y2})
            
            if len(candidates) >= max_candidates:
                break
        if len(candidates) >= max_candidates:
            break
    
    # Add L-shaped candidates (combine adjacent rectangles)
    for i in range(len(candidates)-1):
        c1, c2 = candidates[i], candidates[i+1]
        if len(candidates) >= max_candidates:
            break
        if c1["type"] == "rect" and c2["type"] == "rect":
            if c1["x1"] <= c2["x2"] and c2["x1"] <= c1["x2"]:
                new_x1 = min(c1["x1"], c2["x1"])
                new_x2 = max(c1["x2"], c2["x2"])
                new_y1 = min(c1["y1"], c2["y1"])
                new_y2 = max(c1["y2"], c2["y2"])
                candidates.append({"type": "L", "x1": new_x1, "y1": new_y1, "x2": new_x2, "y2": new_y2})
                if len(candidates) >= max_candidates:
                    break
        if len(candidates) >= max_candidates:
            break
    
    return {"candidates": candidates[:max_candidates]}
