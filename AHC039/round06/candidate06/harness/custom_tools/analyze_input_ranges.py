def run(ctx, args):
    names = ctx.list_task_inputs()
    if len(names) < 2:
        return {"note": "need at least 2 input files", "mackerel": {"x_min": 0, "x_max": 0, "y_min": 0, "y_max": 0, "count": 0},
                "sardine": {"x_min": 0, "x_max": 0, "y_min": 0, "y_max": 0, "count": 0}}
    
    df_mackerel = ctx.read_input_df(names[0], nrows=5000)
    df_sardine = ctx.read_input_df(names[1], nrows=5000)
    
    m_min_x, m_max_x = df_mackerel['x'].min(), df_mackerel['x'].max()
    m_min_y, m_max_y = df_mackerel['y'].min(), df_mackerel['y'].max()
    m_count = len(df_mackerel)
    
    s_min_x, s_max_x = df_sardine['x'].min(), df_sardine['x'].max()
    s_min_y, s_max_y = df_sardine['y'].min(), df_sardine['y'].max()
    s_count = len(df_sardine)
    
    # Suggest a safe bounding box (expand slightly to capture edge cases)
    margin = 50
    bbox = {
        "x_min": max(0, int(m_min_x - margin)),
        "x_max": min(100000, int(m_max_x + margin)),
        "y_min": max(0, int(m_min_y - margin)),
        "y_max": min(100000, int(m_max_y + margin)),
        "margin_expanded": True
    }
    
    return {"mackerel": {"x_min": int(m_min_x), "x_max": int(m_max_x), "y_min": int(m_min_y), "y_max": int(m_max_y), "count": m_count},
            "sardine": {"x_min": int(s_min_x), "x_max": int(s_max_x), "y_min": int(s_min_y), "y_max": int(s_max_y), "count": s_count},
            "bbox": bbox,
            "suggestion": "Start with rectangle covering mackerel range: [" + str(int(m_min_x)) + "," + str(int(m_min_y)) + "] to [" + str(int(m_max_x)) + "," + str(int(m_max_y)) + "]"}
