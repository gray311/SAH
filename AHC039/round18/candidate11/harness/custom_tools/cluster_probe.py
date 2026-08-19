def run(ctx, args):
    min_x = args.get("min_x", 0)
    min_y = args.get("min_y", 0)
    max_x = args.get("max_x", 100000)
    max_y = args.get("max_y", 100000)
    
    # Use grid-based counting for fast approximation
    grid_size = 200
    cell_size = 100000 // grid_size
    
    # Parse program to extract fish positions (same as seed)
    program_text = ctx.get_program()
    fish_data = []
    for line in program_text.split('\n'):
        line = line.strip()
        if line.startswith('fish['):
            try:
                parts = line.replace('fish[', '').replace(']', '').split(',')
                if len(parts) >= 2:
                    x, y = int(parts[0]), int(parts[1])
                    fish_type = 1 if 'mackerel' in line.lower() else -1
                    fish_data.append((x, y, fish_type))
            except:
                continue
    
    # Grid counting
    grid = [[{'m': 0, 's': 0} for _ in range(grid_size)] for _ in range(grid_size)]
    for x, y, ftype in fish_data:
        cx, cy = x // cell_size, y // cell_size
        if 0 <= cx < grid_size and 0 <= cy < grid_size:
            if ftype == 1:
                grid[cy][cx]['m'] += 1
            else:
                grid[cy][cx]['s'] += 1
    
    # Count fish in rectangle by summing grid cells
    total_m = 0
    total_s = 0
    for y in range(max(0, min_y // cell_size), min(grid_size, (max_y + cell_size) // cell_size)):
        for x in range(max(0, min_x // cell_size), min(grid_size, (max_x + cell_size) // cell_size)):
            total_m += grid[y][x]['m']
            total_s += grid[y][x]['s']
    
    return {"mackerels": total_m, "sardines": total_s, "score": total_m - total_s}
