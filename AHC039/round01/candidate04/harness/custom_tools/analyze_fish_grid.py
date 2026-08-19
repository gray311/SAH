def run(ctx, args):
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no task inputs"}
    
    # Read mackerel positions
    mackerels = []
    try:
        m_file = ctx.task_input_path("mackerels.csv")
        with ctx.open(m_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    mackerels.append((int(parts[0]), int(parts[1])))
    except:
        pass
    
    # Read sardine positions
    sardines = []
    try:
        s_file = ctx.task_input_path("sardines.csv")
        with ctx.open(s_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    sardines.append((int(parts[0]), int(parts[1])))
    except:
        pass
    
    # Build grid cell counts (100x100 cells for 0-100000 range)
    CELL_SIZE = 100
    mackerel_grid = {}
    sardine_grid = {}
    
    for x, y in mackerels:
        cell_x = x // CELL_SIZE
        cell_y = y // CELL_SIZE
        key = (cell_x, cell_y)
        mackerel_grid[key] = mackerel_grid.get(key, 0) + 1
    
    for x, y in sardines:
        cell_x = x // CELL_SIZE
        cell_y = y // CELL_SIZE
        key = (cell_x, cell_y)
        sardine_grid[key] = sardine_grid.get(key, 0) + 1
    
    return {"mackerel_grid": mackerel_grid, "sardine_grid": sardine_grid,
            "mackerel_count": len(mackerels), "sardine_count": len(sardines)}