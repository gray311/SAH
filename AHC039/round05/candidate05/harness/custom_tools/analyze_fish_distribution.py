def run(ctx, args):
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no inputs", "hint": "use default rectangle 0,0 to 100000,100000"}
    try:
        # Read mackerel positions (first input file)
        data = ctx.read_input_df(names[0], nrows=1000)
        if 'x' not in data or 'y' not in data:
            return {"error": "invalid input format", "hint": "check column names"}
        
        xs = data['x'].values
        ys = data['y'].values
        
        min_x, max_x = int(xs.min()), int(xs.max())
        min_y, max_y = int(ys.min()), int(ys.max())
        
        # Calculate spread for strategy hint
        x_range = max_x - min_x
        y_range = max_y - min_y
        
        # Recommend rectangle corners and strategy
        hint = ""
        if x_range > y_range:
            hint = f"X is wider. Consider L-shape or horizontal rectangle. Vertices: ({min_x},{min_y}) ({max_x},{min_y}) ({max_x},{max_y}) ({min_x},{max_y})"
        else:
            hint = f"Y is wider. Consider vertical rectangle. Vertices: ({min_x},{min_y}) ({max_x},{min_y}) ({max_x},{max_y}) ({min_x},{max_y})"
        
        return {
            "mackerel_count": len(data),
            "mackerel_min_x": min_x,
            "mackerel_min_y": min_y,
            "mackerel_max_x": max_x,
            "mackerel_max_y": max_y,
            "x_range": x_range,
            "y_range": y_range,
            "hint": hint
        }
    except Exception as e:
        return {"error": str(e), "hint": "use default rectangle 0,0 to 100000,100000"}
