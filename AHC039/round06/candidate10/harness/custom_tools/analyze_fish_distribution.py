def run(ctx, args):
    import collections
    import math
    
    # Read all mackerels and sardines
    mackerels = []
    sardines = []
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no inputs"}
    
    # Process each input file
    for fname in names:
        df = ctx.read_input_df(fname, nrows=10000)  # Read up to 10000 points
        if len(df) == 0:
            continue
        
        # Determine if mackerels or sardines (first N are mackerels in typical format)
        # For this task, we know N=5000 each, but we read all and sort
        # Check available columns to avoid KeyError
        if 'x' in df.columns and 'y' in df.columns:
            points = df[['x', 'y']].values.tolist()
            mackerels.extend([(p[0], p[1]) for p in points[:5000]])
            sardines.extend([(p[0], p[1]) for p in points[5000:]])
    
    mackerels = list(set(mackerels))
    sardines = list(set(sardines))
    
    # Create grid for density analysis
    grid_size = 20000  # 20000x20000 grid
    grid = collections.defaultdict(lambda: {"mackerel": 0, "sardine": 0})
    
    # Bin points
    for mx, my in mackerels:
        gx = min(grid_size - 1, max(0, int(mx / grid_size * grid_size)))
        gy = min(grid_size - 1, max(0, int(my / grid_size * grid_size)))
        grid[(gx, gy)]["mackerel"] += 1
    
    for sx, sy in sardines:
        gx = min(grid_size - 1, max(0, int(sx / grid_size * grid_size)))
        gy = min(grid_size - 1, max(0, int(sy / grid_size * grid_size)))
        grid[(gx, gy)]["sardine"] += 1
    
    # Find best regions: high mackerel, low sardine
    best_cells = []
    for cell, counts in grid.items():
        if counts["mackerel"] > 0 and counts["sardine"] == 0:
            best_cells.append((counts["mackerel"], cell))
    best_cells.sort(reverse=True)
    
    # Calculate mackerel/sardine density
    m_total = len(mackerels)
    s_total = len(sardines)
    m_per_grid = m_total / (grid_size * grid_size)
    s_per_grid = s_total / (grid_size * grid_size)
    
    return {
        "grid_size": grid_size,
        "total_cells": len(grid),
        "mackerel_cells": sum(1 for c in grid.values() if c["mackerel"] > 0),
        "sardine_cells": sum(1 for c in grid.values() if c["sardine"] > 0),
        "best_mackerel_regions": [
            {"grid_cell": (c[1], c[2]), "mackerel_count": c[0], "sardine_count": grid[(c[1], c[2])]["sardine"]}
            for c in best_cells[:10]
        ],
        "mackerel_density": m_per_grid,
        "sardine_density": s_per_grid,
        "mackerel/sardine_ratio": m_total / s_total if s_total > 0 else float('inf')
    }