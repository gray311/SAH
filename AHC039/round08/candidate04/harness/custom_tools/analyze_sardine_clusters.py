def run(ctx, args):
    cell_size = 200
    grid_size = 500
    grid = [[{'m': 0, 's': 0} for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Parse fish positions from program (simple extraction)
    program_text = ctx.get_program()
    fish_list = []
    for line in program_text.split('\n'):
        line = line.strip()
        if not line or 'fish[' not in line:
            continue
        try:
            parts = line.split(',')
            if len(parts) >= 2:
                x, y, ftype = int(parts[0].replace('fish[', '').strip()), int(parts[1].strip()), 1 if 'mackerel' in line.lower() else -1
                cx, cy = x // cell_size, y // cell_size
                if 0 <= cx < grid_size and 0 <= cy < grid_size:
                    grid[cy][cx]['m' if ftype == 1 else 's'] += 1
                    fish_list.append((x, y, ftype))
        except:
            continue
    
    # Compute scores and find top 15 sardine clusters
    sardine_cells = []
    for cy in range(grid_size):
        for cx in range(grid_size):
            if grid[cy][cx]['s'] > 0:
                sardine_cells.append((cy * grid_size + cx, grid[cy][cx]['s'], 
                                      grid[cy][cx]['m'], 
                                      grid[cy][cx]['m'] - grid[cy][cx]['s']))
    
    sardine_cells.sort(key=lambda t: t[1], reverse=True)
    top_15 = sardine_cells[:15]
    
    return {"sardine_clusters": top_15, "num_clusters": len(top_15)}
