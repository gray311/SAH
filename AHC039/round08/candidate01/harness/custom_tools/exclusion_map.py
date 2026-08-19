def run(ctx, args):
    # Build 200x200 exclusion grid
    grid_size = 200
    cell_size = 100000 // grid_size
    
    # Initialize grid with boundary info
    # Each cell tracks: mackerels_on_edge, sardines_on_edge
    mackerels_on_edge = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    sardines_on_edge = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Read fish from program
    lines = ctx.get_program().split('\n')
    fish_positions = []
    for line in lines:
        line = line.strip()
        if not line or 'fish[' not in line:
            continue
        try:
            # Parse fish position from line
            parts = line.split(',')
            if len(parts) >= 2:
                x, y = int(parts[0].strip().replace('fish[', '').strip()), int(parts[1].strip().replace(']', '').strip())
                fish_type = 'mackerel' if 'mackerel' in line.lower() else 'sardine'
                fish_positions.append((x, y, fish_type))
        except:
            continue
    
    # Populate grid with edge info
    # Cell (cx, cy) represents region [cx*cell_size, (cx+1)*cell_size) x [cy*cell_size, (cy+1)*cell_size)
    for x, y, ftype in fish_positions:
        cx, cy = x // cell_size, y // cell_size
        if 0 <= cx < grid_size and 0 <= cy < grid_size:
            if ftype == 'mackerel':
                mackerels_on_edge[cy][cx] += 1
            else:
                sardines_on_edge[cy][cx] += 1
    
    # Compute exclusion ratio and find top zones
    cells = []
    for cy in range(grid_size):
        for cx in range(grid_size):
            m = mackerels_on_edge[cy][cx]
            s = sardines_on_edge[cy][cx]
            if m + s > 0:
                ratio = s / (s + m)
                cells.append((cx, cy, m, s, ratio))
    
    # Sort by exclusion ratio descending
    cells.sort(key=lambda t: t[4], reverse=True)
    
    # Return top 50 exclusion zones
    top_50 = cells[:50]
    
    return {
        "exclusion_zones": [
            {"x_cell": c[0], "y_cell": c[1], "mackerels": c[2], 
             "sardines": c[3], "exclusion_ratio": round(c[4], 4)}
            for c in top_50
        ],
        "total_zones": len(cells)
    }
