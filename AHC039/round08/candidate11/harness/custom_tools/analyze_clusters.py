def run(ctx, args):
    grid_size = 200
    cell_size = 100000 // grid_size
    grid = [[{'m': 0, 's': 0} for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Populate grid from fish positions
    for i, fish in enumerate(ctx.get_program().split(chr(10))):
        fish = fish.strip()
        if not fish or fish.startswith('fish['):
            continue
        parts = fish.replace('fish[', '').replace(']', '').split(',')
        if len(parts) >= 2:
            try:
                x, y, fish_type = int(parts[0]), int(parts[1]), 1 if 'mackerel' in fish else -1
                cx, cy = x // cell_size, y // cell_size
                if 0 <= cx < grid_size and 0 <= cy < grid_size:
                    grid[cy][cx]['m' if fish_type == 1 else 's'] += 1
            except:
                continue
    
    # Compute scores and find top 10
    cells_with_fish = [(cy * grid_size + cx, grid[cy][cx]['m'] - grid[cy][cx]['s'])
                       for cy in range(grid_size) for cx in range(grid_size)
                       if grid[cy][cx]['m'] + grid[cy][cx]['s'] > 0]
    cells_with_fish.sort(key=lambda t: t[1], reverse=True)
    top_10 = cells_with_fish[:10]
    
    return {"clusters": top_10, "num_clusters": len(top_10)}
