def run(ctx, args):
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no inputs"}
    df = ctx.read_input_df(names[0], nrows=2000)
    
    # Check if 'type' column exists
    if 'type' not in df.columns:
        return {"note": "missing type column"}
    
    mackerels = df[df['type'] == 1]
    sardines = df[df['type'] == -1]
    
    if len(mackerels) == 0:
        return {"boxes": []}
    
    # Tight bounding box of all mackerels in sample
    boxes = []
    boxes.append({
        "label": "all_mackerels",
        "min_x": int(mackerels['x'].min()),
        "max_x": int(mackerels['x'].max()),
        "min_y": int(mackerels['y'].min()),
        "max_y": int(mackerels['y'].max()),
        "mackerel_count": len(mackerels),
        "perimeter_estimate": 2 * ((mackerels['x'].max() - mackerels['x'].min()) + (mackerels['y'].max() - mackerels['y'].min())),
        "type": "box"
    })
    
    # Split by x-median
    mid_x = int(mackerels['x'].median())
    left_m = mackerels[mackerels['x'] <= mid_x]
    right_m = mackerels[mackerels['x'] > mid_x]
    
    if len(left_m) > 0:
        boxes.append({
            "label": "mackerels_left",
            "min_x": int(left_m['x'].min()),
            "max_x": int(left_m['x'].max()),
            "min_y": int(left_m['y'].min()),
            "max_y": int(left_m['y'].max()),
            "mackerel_count": len(left_m),
            "perimeter_estimate": 2 * ((left_m['x'].max() - left_m['x'].min()) + (left_m['y'].max() - left_m['y'].min())),
            "type": "box"
        })
    if len(right_m) > 0:
        boxes.append({
            "label": "mackerels_right",
            "min_x": int(right_m['x'].min()),
            "max_x": int(right_m['x'].max()),
            "min_y": int(right_m['y'].min()),
            "max_y": int(right_m['y'].max()),
            "mackerel_count": len(right_m),
            "perimeter_estimate": 2 * ((right_m['x'].max() - right_m['x'].min()) + (right_m['y'].max() - right_m['y'].min())),
            "type": "box"
        })
    
    return {"num_fish_analyzed": len(mackerels) + len(sardines), "mackerel_count": len(mackerels), "boxes": boxes}