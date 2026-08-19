def run(ctx, args):
    import random
    seed = args.get("seed_ratio", 42)
    random.seed(seed)
    
    patterns = [
        {"idx": 0, "heights": [1.40], "ranges": [[0.25, 0.75]]},
        {"idx": 1, "heights": [1.50], "ranges": [[0.27, 0.73]]},
        {"idx": 2, "heights": [1.60], "ranges": [[0.30, 0.70]]},
        {"idx": 3, "heights": [0.90, 1.90, 0.90], "ranges": [[0.15, 0.25], [0.25, 0.75], [0.75, 0.85]]},
        {"idx": 4, "heights": [1.10, 2.30, 1.40], "ranges": [[0.11, 0.21], [0.21, 0.49], [0.49, 0.71]]},
        {"idx": 5, "heights": [1.50, 1.50], "ranges": [[0.22, 0.38], [0.52, 0.82]]},
        {"idx": 6, "heights": [0.70, 1.30, 1.70, 1.00], "ranges": [[0.06, 0.20], [0.20, 0.34], [0.34, 0.64], [0.64, 0.94]]},
        {"idx": 7, "heights": [0.60, 1.20, 2.20, 1.20, 0.60], "ranges": [[0.12, 0.18], [0.18, 0.28], [0.28, 0.72], [0.72, 0.82], [0.82, 0.88]]},
        {"idx": 8, "heights": [0.60, 1.00, 1.50, 1.20], "ranges": [[0.06, 0.24], [0.24, 0.44], [0.44, 0.64], [0.64, 0.94]]},
        {"idx": 9, "heights": [1.20, 2.80], "ranges": [[0.10, 0.90], [0.35, 0.65]]},
        {"idx": 10, "heights": [1.50, 2.50, 1.50], "ranges": [[0.15, 0.30], [0.30, 0.40], [0.40, 0.50]]},
        {"idx": 11, "heights": [2.50, 2.50], "ranges": [[0.30, 0.40], [0.50, 0.60]]}
    ]
    
    pa = patterns[args.get("pattern_a_idx", 0)]
    pb = patterns[args.get("pattern_b_idx", 1)]
    strategy = args.get("strategy", "height_merge")
    
    if strategy == "height_merge":
        new_heights = [0.0] * (len(pa["heights"]) + len(pb["heights"]))
        new_heights[:len(pa["heights"])] = pa["heights"]
        new_heights[len(pa["heights"]):] = pb["heights"]
        new_ranges = pa["ranges"] + pb["ranges"]
        
    elif strategy == "range_swap":
        new_heights = pa["heights"]
        new_ranges = pb["ranges"]
        
    elif strategy == "asymmetry_injection":
        if len(pa["heights"]) > 1 and pa["heights"][0] == pa["heights"][-1]:
            new_heights = pa["heights"][:-1] + [pa["heights"][-1] * 1.2]
            new_ranges = pa["ranges"]
        else:
            new_heights = pa["heights"]
            new_ranges = pa["ranges"]
            
    elif strategy == "multi_level_concat":
        new_heights = [pa["heights"][i] if i % 2 == 0 else pb["heights"][i//2] 
                      for i in range(max(len(pa["heights"]), len(pb["heights"])))]
        new_ranges = []
        for h in new_heights:
            if h in pa["heights"]:
                new_ranges.append(pa["ranges"][pa["heights"].index(h)])
            elif h in pb["heights"]:
                new_ranges.append(pb["ranges"][pb["heights"].index(h)])
            else:
                new_ranges.append(pa["ranges"][0])
    
    return {
        "hybrid_pattern": {
            "heights": new_heights,
            "ranges": new_ranges,
            "pattern_a_idx": args.get("pattern_a_idx", 0),
            "pattern_b_idx": args.get("pattern_b_idx", 1),
            "strategy": strategy
        },
        "note": "Created hybrid from patterns " + str(args.get("pattern_a_idx", 0)) + " and " + str(args.get("pattern_b_idx", 1))
    }