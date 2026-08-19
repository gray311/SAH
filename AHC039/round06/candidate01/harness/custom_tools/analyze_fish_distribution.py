def run(ctx, args):
    # Read mackerel and sardine coordinates from task input
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no input files found"}
    
    # Read both coordinate files (assume CSV format with x,y columns)
    try:
        mackerel_df = ctx.read_input_df(names[0], nrows=5000)
        sardine_df = ctx.read_input_df(names[1], nrows=5000)
    except Exception as e:
        return {"error": str(e), "note": "failed to read input"}
    
    if len(mackerel_df) == 0 or len(sardine_df) == 0:
        return {"error": "empty data", "note": "could not parse input"}
    
    # Compute bounding boxes for each type
    mackerel_bbox = {
        'min_x': int(mackerel_df['x'].min()),
        'max_x': int(mackerel_df['x'].max()),
        'min_y': int(mackerel_df['y'].min()),
        'max_y': int(mackerel_df['y'].max())
    }
    sardine_bbox = {
        'min_x': int(sardine_df['x'].min()),
        'max_x': int(sardine_df['x'].max()),
        'min_y': int(sardine_df['y'].min()),
        'max_y': int(sardine_df['y'].max())
    }
    
    # Find center points
    mackerel_center = {
        'x': int(mackerel_df['x'].mean()),
        'y': int(mackerel_df['y'].mean())
    }
    sardine_center = {
        'x': int(sardine_df['x'].mean()),
        'y': int(sardine_df['y'].mean())
    }
    
    # Estimate density (simplified: variance proxy for spread)
    mackerel_spread = {
        'x_spread': float(mackerel_df['x'].std()),
        'y_spread': float(mackerel_df['y'].std())
    }
    sardine_spread = {
        'x_spread': float(sardine_df['x'].std()),
        'y_spread': float(sardine_df['y'].std())
    }
    
    # Identify quadrants and which type dominates each
    mid_x = (mackerel_bbox['max_x'] - mackerel_bbox['min_x']) / 2 + mackerel_bbox['min_x']
    mid_y = (mackerel_bbox['max_y'] - mackerel_bbox['min_y']) / 2 + mackerel_bbox['min_y']
    
    # Count fish per quadrant (sample for speed)
    mackerel_q1 = ((mackerel_df['x'] <= mid_x) & (mackerel_df['y'] >= mid_y)).sum()
    mackerel_q2 = ((mackerel_df['x'] > mid_x) & (mackerel_df['y'] >= mid_y)).sum()
    mackerel_q3 = ((mackerel_df['x'] > mid_x) & (mackerel_df['y'] < mid_y)).sum()
    mackerel_q4 = ((mackerel_df['x'] <= mid_x) & (mackerel_df['y'] < mid_y)).sum()
    
    sardine_q1 = ((sardine_df['x'] <= mid_x) & (sardine_df['y'] >= mid_y)).sum()
    sardine_q2 = ((sardine_df['x'] > mid_x) & (sardine_df['y'] >= mid_y)).sum()
    sardine_q3 = ((sardine_df['x'] > mid_x) & (sardine_df['y'] < mid_y)).sum()
    sardine_q4 = ((sardine_df['x'] <= mid_x) & (sardine_df['y'] < mid_y)).sum()
    
    # Determine best regions (mackerel-dense, sardine-sparse)
    quadrant_scores = [
        (1, mackerel_q1, sardine_q1),
        (2, mackerel_q2, sardine_q2),
        (3, mackerel_q3, sardine_q3),
        (4, mackerel_q4, sardine_q4)
    ]
    quadrant_info = []
    for q, mk, sd in quadrant_scores:
        # High score = many mackerels, few sardines
        score = mk - sd
        quadrant_info.append({
            'quadrant': q,
            'mackerels': int(mk),
            'sardines': int(sd),
            'score': float(score),
            'favorable': score > 10  # Threshold for favorable
        })
    
    # Return comprehensive analysis
    return {
        'analysis_type': 'fish_distribution',
        'mackerels': {
            'count': len(mackerel_df),
            'bounding_box': mackerel_bbox,
            'center': mackerel_center,
            'spread': mackerel_spread,
            'quadrant_counts': {q: dict(c) for q, c in [(i, {'mackerels': ci['mackerels'], 'sardines': ci['sardines'], 'score': ci['score'], 'favorable': ci['favorable']}) for i, ci in enumerate(quadrant_info)]}
        },
        'sardines': {
            'count': len(sardine_df),
            'bounding_box': sardine_bbox,
            'center': sardine_center,
            'spread': sardine_spread
        },
        'quadrant_analysis': quadrant_info,
        'recommendation': 'Focus polygon construction on quadrants with positive (mackerel - sardine) score, particularly those marked as favorable (score > 10)'
    }
