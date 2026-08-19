def run(ctx, args):
    import json
    
    min_x = args.get("min_x", 0)
    max_x = args.get("max_x", 100000)
    min_y = args.get("min_y", 0)
    max_y = args.get("max_y", 100000)
    
    if min_x >= max_x or min_y >= max_y:
        return {"m_count": 0, "s_count": 0, "score": 0}
    
    # Parse program to extract fish positions
    program_text = ctx.get_program()
    mackerels = set()
    sardines = set()
    
    for line in program_text.split('\n'):
        line = line.strip()
        if line.startswith('fish['):
            try:
                parts = line.replace('fish[', '').replace(']', '').split(',')
                if len(parts) >= 2:
                    x, y = int(parts[0]), int(parts[1])
                    fish_type = 1 if 'mackerel' in line.lower() else -1
                    if fish_type == 1:
                        mackerels.add((x, y))
                    else:
                        sardines.add((x, y))
            except:
                continue
    
    if not mackerels and not sardines:
        return {"m_count": 0, "s_count": 0, "score": 0}
    
    # Build grid for O(1) rectangle queries
    grid_size = 200
    cell_size = 100000 // grid_size
    grid = [[{'m': 0, 's': 0} for _ in range(grid_size)] for _ in range(grid_size)]
    for x, y in mackerels:
        cx, cy = x // cell_size, y // cell_size
        if 0 <= cx < grid_size and 0 <= cy < grid_size:
            grid[cy][cx]['m'] += 1
    for x, y in sardines:
        cx, cy = x // cell_size, y // cell_size
        if 0 <= cx < grid_size and 0 <= cy < grid_size:
            grid[cy][cx]['s'] += 1
    
    # Count fish in rectangle using grid
    m_count, s_count = 0, 0
    for cy in range(max(0, min_y // cell_size), min(grid_size, (max_y + cell_size - 1) // cell_size + 1)):
        for cx in range(max(0, min_x // cell_size), min(grid_size, (max_x + cell_size - 1) // cell_size + 1)):
            m_count += grid[cy][cx]['m']
            s_count += grid[cy][cx]['s']
    
    return {"m_count": m_count, "s_count": s_count, "score": m_count - s_count}