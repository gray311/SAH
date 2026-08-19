def run(ctx, args):
    x_min = args.get('x_min', 0)
    x_max = args.get('x_max', 100000)
    y_min = args.get('y_min', 0)
    y_max = args.get('y_max', 100000)
    
    names = ctx.list_task_inputs()
    if not names:
        return {"mackerel": 0, "sardine": 0, "score": 1}
    
    import numpy as np
    df = ctx.read_input_df(names[0], nrows=10000)
    
    mackerel_count = 0
    sardine_count = 0
    for _, row in df.iterrows():
        x, y = int(row.iloc[0]), int(row.iloc[1])
        if x_min <= x <= x_max and y_min <= y <= y_max:
            if row.name < 5000:
                mackerel_count += 1
            else:
                sardine_count += 1
    
    score = max(0, mackerel_count - sardine_count + 1)
    return {"mackerel": mackerel_count, "sardine": sardine_count, "score": score}
