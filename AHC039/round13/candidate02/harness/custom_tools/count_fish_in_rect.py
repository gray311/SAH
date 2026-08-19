def run(ctx, args):
    import bisect
    import json

    x1 = args.get("x1")
    y1 = args.get("y1")
    x2 = args.get("x2")
    y2 = args.get("y2")

    # Get fish positions from input
    names = ctx.list_task_inputs()
    if not names:
        return {"error": "no task inputs", "mackerels_in_rect": 0, "sardines_in_rect": 0}

    input_text = ctx.read_input_sample(names[0], nrows=10000)
    
    mackerels_x = []
    mackerels_y = []
    sardines_x = []
    sardines_y = []
    
    lines = input_text.split('\n')
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 2:
            try:
                x, y = int(parts[0]), int(parts[1])
                if i < 5000:
                    mackerels_x.append(x)
                    mackerels_y.append(y)
                else:
                    sardines_x.append(x)
                    sardines_y.append(y)
            except:
                continue

    # Filter to rectangle [x1, y1] to [x2, y2]
    m_in = 0
    for mx, my in zip(mackerels_x, mackerels_y):
        if x1 is not None and x2 is not None and y1 is not None and y2 is not None:
            if x1 <= mx <= x2 and y1 <= my <= y2:
                m_in += 1
    
    s_in = 0
    for sx, sy in zip(sardines_x, sardines_y):
        if x1 is not None and x2 is not None and y1 is not None and y2 is not None:
            if x1 <= sx <= x2 and y1 <= sy <= y2:
                s_in += 1

    return {
        "mackerels_in_rect": m_in,
        "sardines_in_rect": s_in,
        "score": m_in - s_in
    }