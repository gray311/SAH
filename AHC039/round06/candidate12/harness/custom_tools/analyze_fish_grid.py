def run(ctx, args):
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no task inputs"}
    # Read first 2000 fish points
    sample_size = 2000
    x_vals, y_vals = [], []
    for i in range(sample_size):
        # Parse input - assume coordinates are sequential
        line = ctx.scratch_read("fish_coords")
        if line:
            parts = line.split()
            if len(parts) >= 2:
                try:
                    x_vals.append(int(parts[0]))
                    y_vals.append(int(parts[1]))
                except ValueError:
                    pass
    
    if len(x_vals) < 10:
        return {"note": "insufficient data"}
    
    # Calculate bounding box for mackerels (assume first N are mackerels)
    mackerel_n = len(ctx.get_program()) // 2  # Rough estimate
    min_x, max_x = min(x_vals[:mackerel_n]), max(x_vals[:mackerel_n])
    min_y, max_y = min(y_vals[:mackerel_n]), max(y_vals[:mackerel_n])
    
    # Calculate statistics
    mackerel_count = mackerel_n
    sardine_count = sample_size - mackerel_count
    
    # Perimeter estimate
    perimeter = 2 * (max_x - min_x + max_y - min_y)
    
    # Recommend safe rectangle (shrink by 10% to avoid edge sardines)
    margin_x = max(0, int((max_x - min_x) * 0.1))
    margin_y = max(0, int((max_y - min_y) * 0.1))
    rec_x1 = min_x + margin_x
    rec_y1 = min_y + margin_y
    rec_x2 = max_x - margin_x
    rec_y2 = max_y - margin_y
    
    return {
        "sample_size": sample_size,
        "mackerel_count": mackerel_count,
        "sardine_count": sardine_count,
        "bbox_mackerel": {"min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y},
        "perimeter_estimate": perimeter,
        "recommended_rect": {"x1": rec_x1, "y1": rec_y1, "x2": rec_x2, "y2": rec_y2},
        "note": "Use recommended_rect for initial rectangle; try variants around it"
    }