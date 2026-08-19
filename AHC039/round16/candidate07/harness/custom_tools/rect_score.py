def run(ctx, args):
    import json
    min_x = args.get("min_x", 0)
    min_y = args.get("min_y", 0)
    max_x = args.get("max_x", 100000)
    max_y = args.get("max_y", 100000)
    
    # Parse fish coordinates from the program text
    program_text = ctx.get_program()
    fish_data = []
    coord_count = 0
    
    for line in program_text.split('\n'):
        import re
        coords = re.findall(r'(\d+)\s*,\s*(\d+)', line)
        for cx, cy in coords:
            cx, cy = int(cx), int(cy)
            coord_count += 1
            # First 5000 coordinates = mackerels, next 5000 = sardines
            if coord_count <= 5000:
                fish_data.append((cx, cy, 1))
            else:
                fish_data.append((cx, cy, -1))
    
    if not fish_data:
        return {"error": "no fish data found", "score": 0, "valid": False}
    
    max_coord = 100000
    grid_m = [[0] * (max_coord + 2) for _ in range(max_coord + 2)]
    grid_s = [[0] * (max_coord + 2) for _ in range(max_coord + 2)]
    
    for fx, fy, ftype in fish_data:
        if 0 <= fx <= max_coord and 0 <= fy <= max_coord:
            if ftype == 1:
                grid_m[fy][fx] += 1
            else:
                grid_s[fy][fx] += 1
    
    # Compute prefix sums
    for y in range(max_coord + 2):
        for x in range(max_coord + 2):
            grid_m[y][x] += grid_m[y-1][x] + grid_m[y][x-1] - grid_m[y-1][x-1]
            grid_s[y][x] += grid_s[y-1][x] + grid_s[y][x-1] - grid_s[y-1][x-1]
    
    def query_rect_mx(my, mx, n_y, n_x, grid):
        if my > n_y or mx > n_x:
            return 0
        return grid[n_y][n_x] - grid[my-1][n_x] - grid[n_y][mx-1] + grid[my-1][mx-1]
    
    m_count = query_rect_mx(min_y, min_x, max_y, max_x, grid_m)
    s_count = query_rect_mx(min_y, min_x, max_y, max_x, grid_s)
    
    score = max(0, m_count - s_count + 1)
    return {"score": score, "m_count": m_count, "s_count": s_count, "valid": True}
