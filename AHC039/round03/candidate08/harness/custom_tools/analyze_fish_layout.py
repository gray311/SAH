def run(ctx, args):
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no task inputs found"}
    df = ctx.read_input_df(names[0], nrows=2000)
    if df.empty:
        return {"note": "empty input"}
    x_vals = df.iloc[:, 0] if len(df.columns) > 0 else []
    y_vals = df.iloc[:, 1] if len(df.columns) > 1 else []
    return {"file": names[0], "rows": len(df),
            "x_min": int(df.iloc[:, 0].min()) if len(x_vals) > 0 else 0,
            "x_max": int(df.iloc[:, 0].max()) if len(x_vals) > 0 else 100000,
            "y_min": int(df.iloc[:, 1].min()) if len(y_vals) > 0 else 0,
            "y_max": int(df.iloc[:, 1].max()) if len(y_vals) > 0 else 100000,
            "note": "Use these bounds to guide polygon expansion"}
