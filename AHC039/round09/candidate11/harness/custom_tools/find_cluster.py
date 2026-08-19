def run(ctx, args):
    cluster_type = args.get("cluster_type", "x_based")
    width = args.get("width", 100)
    height = args.get("height", 100)
    
    # Parse program to extract fish positions
    program_text = ctx.get_program()
    mackerels = []
    sardines = set()
    
    for line in program_text.split('\n'):
        line = line.strip()
        if line.startswith('mackerels['):
            try:
                content = line.replace('mackerels[', '').replace(']', '').replace('"', '')
                coords = [int(x.strip()) for x in content.split(',')]
                if len(coords) >= 2:
                    mackerels.append((coords[0], coords[1]))
            except:
                continue
        elif line.startswith('sardines['):
            try:
                content = line.replace('sardines[', '').replace(']', '').replace('"', '')
                coords = [int(x.strip()) for x in content.split(',')]
                if len(coords) >= 2:
                    sardines.add((coords[0], coords[1]))
            except:
                continue
    
    if not mackerels:
        return {"error": "no mackerels found", "cluster": None}
    
    # Find cluster
    best_cluster = None
    best_score = float("-inf")
    
    if cluster_type == "x_based":
        # Group by x-coordinate
        x_groups = {}
        for mx, my in mackerels:
            x_key = mx // width * width
            if x_key not in x_groups:
                x_groups[x_key] = {"x_min": mx, "x_max": mx, "y_min": float("inf"), "y_max": float("-inf")}
            x_groups[x_key]["x_min"] = min(x_groups[x_key]["x_min"], mx)
            x_groups[x_key]["x_max"] = max(x_groups[x_key]["x_max"], mx)
            x_groups[x_key]["y_min"] = min(x_groups[x_key]["y_min"], my)
            x_groups[x_key]["y_max"] = max(x_groups[x_key]["y_max"], my)
            x_groups[x_key]["count"] = x_groups[x_key].get("count", 0) + 1
        
        for x_key, group in x_groups.items():
            s_count = 0
            for mx in range(group["x_min"], group["x_max"] + 1, width):
                for my in range(group["y_min"], group["y_max"] + 1, height):
                    if (mx, my) in sardines:
                        s_count += 1
            
            score = group["count"] - s_count
            if score > best_score:
                best_score = score
                best_cluster = {
                    "x_min": group["x_min"], "x_max": group["x_max"],
                    "y_min": group["y_min"], "y_max": group["y_max"],
                    "count": group["count"], "sardines": s_count
                }
    else:
        # Group by y-coordinate
        y_groups = {}
        for mx, my in mackerels:
            y_key = my // height * height
            if y_key not in y_groups:
                y_groups[y_key] = {"y_min": my, "y_max": my, "x_min": float("inf"), "x_max": float("-inf")}
            y_groups[y_key]["y_min"] = min(y_groups[y_key]["y_min"], my)
            y_groups[y_key]["y_max"] = max(y_groups[y_key]["y_max"], my)
            y_groups[y_key]["x_min"] = min(y_groups[y_key]["x_min"], mx)
            y_groups[y_key]["x_max"] = max(y_groups[y_key]["x_max"], mx)
            y_groups[y_key]["count"] = y_groups[y_key].get("count", 0) + 1
        
        for y_key, group in y_groups.items():
            s_count = 0
            for mx in range(group["x_min"], group["x_max"] + 1, width):
                for my in range(group["y_min"], group["y_max"] + 1, height):
                    if (mx, my) in sardines:
                        s_count += 1
            
            score = group["count"] - s_count
            if score > best_score:
                best_score = score
                best_cluster = {
                    "x_min": group["x_min"], "x_max": group["x_max"],
                    "y_min": group["y_min"], "y_max": group["y_max"],
                    "count": group["count"], "sardines": s_count
                }
    
    if best_cluster:
        return {
            "cluster": best_cluster,
            "score": best_score,
            "vertices": [
                (best_cluster["x_min"], best_cluster["y_min"]),
                (best_cluster["x_max"], best_cluster["y_min"]),
                (best_cluster["x_max"], best_cluster["y_max"]),
                (best_cluster["x_min"], best_cluster["y_max"])
            ]
        }
    else:
        return {"error": "no valid cluster found", "cluster": None}
