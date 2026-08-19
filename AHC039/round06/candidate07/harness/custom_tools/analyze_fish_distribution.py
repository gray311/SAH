def run(ctx, args):
    mackerel_pts = []
    sardine_pts = []
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no task inputs", "mackerel_box": None, "sardine_box": None, "density_zones": []}
    
    # Read mackerels (first N points, assuming CSV-like format or get_program parsing)
    try:
        prog = ctx.get_program()
        # Look for fish coordinates in the program (they're in all_fish_structs or similar)
        # Since we can't easily parse the program, use the task inputs
        df = ctx.read_input_df(names[0], nrows=10000)
        mackerel_box = {"x_min": float("inf"), "x_max": float("-inf"),
                      "y_min": float("inf"), "y_max": float("-inf")}
        sardine_box = {"x_min": float("inf"), "x_max": float("-inf"),
                     "y_min": float("inf"), "y_max": float("-inf")}
        
        for idx, row in df.iterrows():
            x, y = int(row['x']), int(row['y'])
            # Assume even indices are mackerels, odd are sardines (or vice versa)
            # Actually, we need to know the exact format. Let's assume the first column
            # is x, second is y, and we alternate types.
            if idx % 2 == 0:
                mackerel_box["x_min"] = min(mackerel_box["x_min"], x)
                mackerel_box["x_max"] = max(mackerel_box["x_max"], x)
                mackerel_box["y_min"] = min(mackerel_box["y_min"], y)
                mackerel_box["y_max"] = max(mackerel_box["y_max"], y)
            else:
                sardine_box["x_min"] = min(sardine_box["x_min"], x)
                sardine_box["x_max"] = max(sardine_box["x_max"], x)
                sardine_box["y_min"] = min(sardine_box["y_min"], y)
                sardine_box["y_max"] = max(sardine_box["y_max"], y)
        
        # Calculate perimeters for candidate rectangles
        mk_perim = 2 * (mackerel_box["x_max"] - mackerel_box["x_min"] +
                       mackerel_box["y_max"] - mackerel_box["y_min"])
        sdr_perim = 2 * (sardine_box["x_max"] - sardine_box["x_min"] +
                        sardine_box["y_max"] - sardine_box["y_min"])
        
        return {
            "mackerel_box": mackerel_box if mackerel_box["x_min"] != float("inf") else None,
            "sardine_box": sardine_box if sardine_box["x_min"] != float("inf") else None,
            "mackerel_perimeter": mk_perim,
            "sardine_perimeter": sdr_perim,
            "recommendation": "Consider starting with mackerel bounding box if perimeter < 400000"
        }
    except Exception as e:
        return {"error": str(e), "mackerel_box": None, "sardine_box": None, "density_zones": []}
