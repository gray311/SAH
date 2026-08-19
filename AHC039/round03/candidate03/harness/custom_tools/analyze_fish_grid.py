def run(ctx, args):
    mackerels = ctx.get_program()
    import re
    coords = []
    matches = re.findall(r'[0-9]{1,6}\s*[,\s]+[0-9]{1,6}', mackerels)
    for m in matches:
        parts = [int(x) for x in m.split()]
        if len(parts) == 2 and 0 <= parts[0] <= 100000 and 0 <= parts[1] <= 100000:
            coords.append((parts[0], parts[1]))
    if len(coords) < 4:
        return {"note": "not enough coordinate data in program", "suggestion": "hardcode a simple bounding box"}
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    unique_x = sorted(set(xs))
    unique_y = sorted(set(ys))
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    grid_cells = set()
    for (x, y) in coords:
        cell_x = min(unique_x, key=lambda vx: abs(vx - x))
        cell_y = min(unique_y, key=lambda vy: abs(vy - y))
        grid_cells.add((cell_x, cell_y))
    return {
        "min_x": min_x, "max_x": max_x,
        "min_y": min_y, "max_y": max_y,
        "unique_x_count": len(unique_x),
        "unique_y_count": len(unique_y),
        "grid_cells_count": len(grid_cells),
        "suggest_stripes": len(unique_x) > len(unique_y) * 2,
        "suggest_grid": len(unique_x) > 100 or len(unique_y) > 100
    }
