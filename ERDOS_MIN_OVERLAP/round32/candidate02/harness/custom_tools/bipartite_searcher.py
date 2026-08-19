def run(ctx, args):
    import numpy as np
    num_thresholds = args.get("num_thresholds", 10)
    t_min = args.get("threshold_range", {}).get("min", 0.7)
    t_max = args.get("threshold_range", {}).get("max", 1.3)
    
    # Get current program to extract num_intervals
    h_text = ctx.get_best_program()
    if h_text is None or h_text == "":
        return {"error": "No best program available"}
    
    # Extract num_intervals from the program
    import re
    match = re.search(r'num_intervals:\s*(\d+)', h_text)
    if not match:
        return {"error": "Could not extract num_intervals from program"}
    
    num_intervals = int(match.group(1))
    domain = 2.0
    
    thresholds = np.linspace(t_min, t_max, num_thresholds)
    h_candidates = []
    
    for t in thresholds:
        # Create bipartite function: h(x) = 1 if x < t, else 0
        x = np.linspace(0, domain, num_intervals)
        h = np.where(x < t, 1.0, 0.0)
        h_candidates.append(h)
    
    return {
        "candidates": h_candidates,
        "thresholds_used": thresholds.tolist(),
        "num_intervals": num_intervals,
        "note": f"Generated {len(h_candidates)} bipartite candidates with thresholds {t_min:.2f}-{t_max:.2f}"
    }
