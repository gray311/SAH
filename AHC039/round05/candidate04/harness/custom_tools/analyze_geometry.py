def run(ctx, args):
    import math
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no inputs"}
    df = ctx.read_input_df(names[0], nrows=2000)
    
    if len(df) == 0:
        return {"mackerel_box": None, "sardine_box": None, 
                "sardines_in_mackerel_box": 0, "recommendation": "No data"}
    
    x_vals = df.iloc[:, 0].tolist()
    y_vals = df.iloc[:, 1].tolist()
    
    mackerel_points = []
    sardine_points = []
    
    for i in range(min(len(df), 2000)):
        if i % 2 == 0:
            mackerel_points.append((int(x_vals[i]), int(y_vals[i])))
        else:
            sardine_points.append((int(x_vals[i]), int(y_vals[i])))
    
    def get_bbox(points):
        if len(points) == 0:
            return None
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)
        width = max_x - min_x
        height = max_y - min_y
        perimeter = 2 * (width + height)
        return {"min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y,
                "width": width, "height": height, "perimeter": perimeter}
    
    mack_box = get_bbox(mackerel_points)
    sard_box = get_bbox(sardine_points)
    
    sardines_in_box = 0
    if sard_box and mack_box:
        x_overlap = max(0, min(sard_box["max_x"], mack_box["max_x"]) - 
                       max(sard_box["min_x"], mack_box["min_x"]))
        y_overlap = max(0, min(sard_box["max_y"], mack_box["max_y"]) - 
                       max(sard_box["min_y"], mack_box["min_y"]))
        area_sard = (sard_box["max_x"] - sard_box["min_x"]) * \
                   (sard_box["max_y"] - sard_box["min_y"]) + 1
        if area_sard > 0:
            overlap_frac = (x_overlap * y_overlap) / area_sard
            sardines_in_box = int(len(sardine_points) * overlap_frac)
    
    rec = []
    if mack_box:
        rec.append("Use mackerel bounding box: [{}, {}] x [{}, {}], perimeter: {}".format(
            mack_box["min_x"], mack_box["max_x"], mack_box["min_y"], mack_box["max_y"], 
            mack_box["perimeter"]))
    
    if sardines_in_box > 150:
        rec.append("HIGH SARDINE OVERLAP: Consider smaller, tighter polygon around dense clusters")
    elif sardines_in_box < 50:
        rec.append("LOW SARDINE OVERLAP: Large bounding box likely effective")
    else:
        rec.append("MODERATE OVERLAP: Try cluster-based approach or exclude sardine-rich regions")
    
    return {
        "mackerel_box": mack_box,
        "sardine_box": sard_box,
        "sardines_in_mackerel_box": sardines_in_box,
        "recommendation": rec
    }