def run(ctx, args):
    # Read fish data
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no inputs"}
    
    # Load all fish
    fish_data = ctx.read_input_df(names[0], nrows=10000)  # 5000 mackerels + 5000 sardines
    
    if len(fish_data) != 10000:
        return {"note": f"unexpected fish count: {len(fish_data)}"}
    
    # Build 100x100 grid
    G = 100
    max_coord = 100000
    cell_size = max_coord / G
    
    grid = {}  # (row, col) -> {"mackerel": 0, "sardine": 0}
    
    for _, row in fish_data.iterrows():
        x, y, fish_type = int(row['x']), int(row['y']), int(row['type'])
        row_idx = int(y / cell_size)
        col_idx = int(x / cell_size)
        cell = (row_idx, col_idx)
        if cell not in grid:
            grid[cell] = {"mackerel": 0, "sardine": 0}
        if fish_type == 1:
            grid[cell]["mackerel"] += 1
        else:
            grid[cell]["sardine"] += 1
    
    # Compute ratios and sort
    cell_ratios = []
    for (r, c), counts in grid.items():
        m = counts["mackerel"]
        s = counts["sardine"]
        ratio = m / (s + 1)  # avoid division by zero
        cell_ratios.append({
            "row": r, "col": c,
            "mackerel": m, "sardine": s,
            "ratio": ratio,
            "score": m - s + 1
        })
    
    # Sort by ratio descending
    cell_ratios.sort(key=lambda x: x["ratio"], reverse=True)
    
    # Return top K
    K = min(args.get("K", 500), len(cell_ratios))
    top_cells = cell_ratios[:K]
    
    # Statistics
    total_m = sum(c["mackerel"] for c in cell_ratios)
    total_s = sum(c["sardine"] for c in cell_ratios)
    
    return {
        "num_cells": len(grid),
        "top_cells": top_cells,
        "statistics": {
            "total_mackerels": total_m,
            "total_sardines": total_s,
            "max_ratio": max((c["ratio"] for c in cell_ratios), default=0),
            "min_ratio": min((c["ratio"] for c in cell_ratios), default=0),
            "mean_ratio": sum(c["ratio"] for c in cell_ratios) / len(cell_ratios) if cell_ratios else 0
        }
    }
