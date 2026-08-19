def run(ctx, args):
    import math
    top_k = args.get("top_k_regions", 5)
    cell_size = args.get("region_size", 500)
    
    # Get task inputs
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no task inputs", "density_regions": []}
    
    # Create a grid density map
    density_grid = {}
    for idx in range(len(names)):
        name = names[idx]
        try:
            df = ctx.read_input_df(name, nrows=5000)
            mackerels = df.iloc[:2500].values if len(df) >= 5000 else df.values
            for _, row in mackerels.iterrows():
                x, y = int(row[0]), int(row[1])
                cell_x = x // cell_size
                cell_y = y // cell_size
                key = (cell_x, cell_y)
                density_grid[key] = density_grid.get(key, 0) + 1
        except:
            pass
    
    # Sort by density and return top regions
    sorted_regions = sorted(density_grid.items(), key=lambda x: -x[1])[:top_k]
    regions = [{"cell": (c[0], c[1]), "density": c[1]} for c in sorted_regions]
    
    # Return centroid info for each dense region
    centroids = []
    for (cx, cy), count in regions:
        x_low = cx * cell_size; x_high = (cx + 1) * cell_size
        y_low = cy * cell_size; y_high = (cy + 1) * cell_size
        centroids.append({
            "center_x": int((x_low + x_high) / 2),
            "center_y": int((y_low + y_high) / 2),
            "dense_cells": count
        })
    
    return {
        "top_dense_regions": regions,
        "centroids": centroids,
        "total_cells_analyzed": len(density_grid)
    }
