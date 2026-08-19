def run(ctx, args):
    import math
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no inputs found"}
    
    input_file = names[0]
    df = ctx.read_input_df(input_file, nrows=10000)
    
    # Check if 'type' column exists before filtering
    if 'type' not in df.columns:
        return {"note": "missing type column"}
    
    mackerels = df[df['type'] == 1]
    sardines = df[df['type'] == -1]
    
    result = {
        "file": input_file,
        "n_mackerels": int(len(mackerels)),
        "n_sardines": int(len(sardines)),
        "mackerel_x_range": [int(mackerels['x'].min()), int(mackerels['x'].max())],
        "mackerel_y_range": [int(mackerels['y'].min()), int(mackerels['y'].max())],
        "sardine_x_range": [int(sardines['x'].min()), int(sardines['x'].max())],
        "sardine_y_range": [int(sardines['y'].min()), int(sardines['y'].max())],
        "mackerel_centroid": [float(mackerels['x'].mean()), float(mackerels['y'].mean())],
        "sardine_centroid": [float(sardines['x'].mean()), float(sardines['y'].mean())]
    }
    
    # Simple clustering hint based on coordinate spread
    m_x_span = result["mackerel_x_range"][1] - result["mackerel_x_range"][0]
    s_x_span = result["sardine_x_range"][1] - result["sardine_x_range"][0]
    
    result["cluster_overlap_x"] = "HIGH" if abs(m_x_span - s_x_span) < 50000 else "MODERATE"
    
    return result