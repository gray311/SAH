def run(ctx, args):
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no inputs"}
    df = ctx.read_input_df(names[0], nrows=5000)
    x = df.iloc[:, 0]
    y = df.iloc[:, 1]
    x_min, x_max = int(x.min()), int(x.max())
    y_min, y_max = int(y.min()), int(y.max())
    cell_size = max(100, (x_max - x_min) / 200)
    if (x_max - x_min) / cell_size < 50 and (y_max - y_min) / cell_size < 50:
        approach = "corner-pair"
        candidates = (x_max - x_min) * (y_max - y_min)
    else:
        approach = "grid-sweep"
        candidates = ((x_max - x_min) / cell_size) * ((y_max - y_min) / cell_size)
    return {
        "approach": approach,
        "candidate_count": int(candidates),
        "cell_size": cell_size,
        "x_range": [x_min, x_max],
        "y_range": [y_min, y_max],
        "recommendation": f"Use {approach} with ~{int(candidates)} candidates"
    }
