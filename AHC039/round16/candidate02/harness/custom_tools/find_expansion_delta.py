def run(ctx, args):
    import json
    rect = args.get("rect")
    direction = args.get("direction")
    expand_amount = args.get("expand_amount", 50)
    
    if rect is None or direction is None:
        return {"error": "Missing rect or direction"}
    
    min_x, min_y = rect["min_x"], rect["min_y"]
    max_x, max_y = rect["max_x"], rect["max_y"]
    
    # Parse program to extract fish positions
    program_text = ctx.get_program()
    fish_data = []
    for line in program_text.split('\n'):
        line = line.strip()
        if line.startswith('fish['):
            try:
                parts = line.replace('fish[', '').replace(']', '').split(',')
                if len(parts) >= 2:
                    x, y = int(parts[0].strip()), int(parts[1].strip())
                    fish_type = 1 if 'mackerel' in line.lower() else -1
                    fish_data.append((x, y, fish_type))
            except:
                continue
    
    # Build grid
    grid_size = 200
    grid = [[{'m': 0, 's': 0} for _ in range(grid_size)] for _ in range(grid_size)]
    cell_size = 100000 // grid_size
    
    for x, y, ftype in fish_data:
        cx, cy = x // cell_size, y // cell_size
        if 0 <= cx < grid_size and 0 <= cy < grid_size:
            if ftype == 1:
                grid[cy][cx]['m'] += 1
            else:
                grid[cy][cx]['s'] += 1
    
    # Precompute prefix sums for fast rectangle queries
    prefix_m = [[0] * (grid_size + 1) for _ in range(grid_size + 1)]
    prefix_s = [[0] * (grid_size + 1) for _ in range(grid_size + 1)]
    
    for r in range(grid_size):
        for c in range(grid_size):
            prefix_m[r + 1][c + 1] = prefix_m[r][c + 1] + prefix_m[r + 1][c] - prefix_m[r][c] + grid[r][c]['m']
            prefix_s[r + 1][c + 1] = prefix_s[r][c + 1] + prefix_s[r + 1][c] - prefix_s[r][c] + grid[r][c]['s']
    
    def query_rect_area(x1, y1, x2, y2):
        if x1 > x2 or y1 > y2:
            return 0, 0
        c1, c2 = max(0, x1 // cell_size), min(grid_size - 1, x2 // cell_size)
        r1, r2 = max(0, y1 // cell_size), min(grid_size - 1, y2 // cell_size)
        if c1 > c2 or r1 > r2:
            return 0, 0
        m = prefix_m[r2 + 1][c2 + 1] - prefix_m[r1][c2 + 1] - prefix_m[r2 + 1][c1] + prefix_m[r1][c1]
        s = prefix_s[r2 + 1][c2 + 1] - prefix_s[r1][c2 + 1] - prefix_s[r2 + 1][c1] + prefix_s[r1][c1]
        return m, s
    
    # Current score
    orig_m, orig_s = query_rect_area(min_x, min_y, max_x, max_y)
    orig_score = orig_m - orig_s
    
    # Direction deltas
    deltas = {"N": (0, expand_amount), "S": (0, -expand_amount), "E": (expand_amount, 0), "W": (-expand_amount, 0)}
    if direction not in deltas:
        return {"error": f"Invalid direction: {direction}"}
    
    dr, dc = deltas[direction]
    
    new_min_x, new_min_y = min_x, min_y
    new_max_x, new_max_y = max_x, max_y
    
    if direction == "N":
        new_max_y = max_y + expand_amount
    elif direction == "S":
        new_max_y = min_y - expand_amount
    elif direction == "E":
        new_max_x = max_x + expand_amount
    elif direction == "W":
        new_max_x = min_x - expand_amount
    
    new_m, new_s = query_rect_area(new_min_x, new_min_y, new_max_x, new_max_y)
    new_score = new_m - new_s
    
    delta = new_score - orig_score
    
    # Check if expansion is reasonable (don't expand too much)
    new_perimeter = 2 * ((new_max_x - new_min_x) + (new_max_y - new_min_y))
    if new_perimeter > 400000:
        return {"delta_score": delta, "valid_expansion": False, "note": "Perimeter exceeds limit"}
    
    return {"delta_score": delta, "valid_expansion": True, "new_m": new_m, "new_s": new_s}
