def run(ctx, args):
    import json
    input_names = ctx.list_task_inputs()
    if not input_names:
        return {"note": "No inputs", "rectangles": []}
    input_name = input_names[0]
    rows = ctx.read_input_sample(input_name, nrows=10000)
    lines = rows.strip().split(chr(10))
    mackerels = []
    sardines = []
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        parts = line.strip().split()
        if len(parts) != 2:
            continue
        try:
            x, y = int(parts[0]), int(parts[1])
            if i < 5000:
                mackerels.append((x, y))
            else:
                sardines.append((x, y))
        except:
            continue
    if not mackerels and not sardines:
        return {"note": "No parsed fish", "rectangles": []}
    all_pts = mackerels + sardines
    min_x = min(p[0] for p in all_pts) if all_pts else 0
    max_x = max(p[0] for p in all_pts) if all_pts else 100000
    min_y = min(p[1] for p in all_pts) if all_pts else 0
    max_y = max(p[1] for p in all_pts) if all_pts else 100000
    rectangles = []
    steps = 100
    for x1 in range(min_x, max_x + 1, max(1, (max_x - min_x) // steps)):
        for x2 in range(x1 + 1, max_x + 1, max(1, (max_x - min_x) // steps)):
            for y1 in range(min_y, max_y + 1, max(1, (max_y - min_y) // steps)):
                for y2 in range(y1 + 1, max_y + 1, max(1, (max_y - min_y) // steps)):
                    m_count = sum(1 for (mx, my) in mackerels if x1 <= mx <= x2 and y1 <= my <= y2)
                    s_count = sum(1 for (sx, sy) in sardines if x1 <= sx <= x2 and y1 <= sy <= y2)
                    net = m_count - s_count
                    if net > 0:
                        rectangles.append({"x1": x1, "y1": y1, "x2": x2, "y2": y2, "mackerels": m_count, "sardines": s_count, "net_gain": net})
    rectangles.sort(key=lambda r: r["net_gain"], reverse=True)
    return {"num_rectangles": len(rectangles), "rectangles": rectangles[:50]}
