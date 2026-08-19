def run(ctx, args):
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no task inputs"}
    # Read all fish positions from the input
    try:
        df_mack = ctx.read_input_df(names[0], nrows=10000)  # First half
        df_sard = ctx.read_input_df(names[1], nrows=10000)  # Second half
    except:
        return {"note": "input read failed"}
    
    mackerels = set()
    sardines = set()
    for _, row in df_mack.iterrows():
        mackerels.add((int(row[0]), int(row[1])))
    for _, row in df_sard.iterrows():
        sardines.add((int(row[0]), int(row[1])))
    
    # Create a coarse grid (e.g., 100x100 cells)
    cell_size = 1000
    grid = {}
    
    for (x, y) in mackerels:
        cx, cy = x // cell_size, y // cell_size
        grid[(cx, cy)] = grid.get((cx, cy), 0) + 1
    
    for (x, y) in sardines:
        cx, cy = x // cell_size, y // cell_size
        grid[(cx, cy)] = grid.get((cx, cy), 0) - 1
    
    # Find best regions
    best_cells = sorted(grid.items(), key=lambda x: -x[1])[:20]
    
    return {
        "mackerel_count": len(mackerels),
        "sardine_count": len(sardines),
        "grid_resolution": cell_size,
        "best_regions": [(c, mc, sc) for c, (mc, sc) in best_cells]
    }
