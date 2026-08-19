def run(ctx, args):
    import random
    pattern_idx = args.get("pattern_idx", random.randint(0, 13))
    height_scale = args.get("height_scale", random.uniform(0.95, 1.15))
    pos_shift = args.get("pos_shift", random.uniform(0.95, 1.05))
    num_variants = args.get("num_variants", random.randint(3, 5))
    
    # Seed patterns: (pattern_name, default_intervals)
    patterns = {
        0: ("high_peak_single", [{"start": 0.25, "end": 0.75, "height": 1.25}]),
        1: ("higher_peak", [{"start": 0.28, "end": 0.72, "height": 1.35}]),
        2: ("very_high_narrow", [{"start": 0.30, "end": 0.70, "height": 1.5}]),
        3: ("multi_level_mid", [{"start": 0.15, "end": 0.25, "height": 0.8},
                                 {"start": 0.25, "end": 0.75, "height": 1.8},
                                 {"start": 0.75, "end": 0.85, "height": 0.8}]),
        4: ("three_level_asym", [{"start": 0.1, "end": 0.2, "height": 1.0},
                                 {"start": 0.2, "end": 0.5, "height": 2.2},
                                 {"start": 0.5, "end": 0.7, "height": 1.3}]),
        5: ("two_high_steps", [{"start": 0.2, "end": 0.4, "height": 1.4},
                               {"start": 0.5, "end": 0.8, "height": 1.4}]),
        6: ("four_level", [{"start": 0.05, "end": 0.2, "height": 0.6},
                           {"start": 0.2, "end": 0.35, "height": 1.2},
                           {"start": 0.35, "end": 0.65, "height": 1.6},
                           {"start": 0.65, "end": 0.95, "height": 0.9}]),
        7: ("narrow_high_wings", [{"start": 0.1, "end": 0.3, "height": 0.7},
                                  {"start": 0.3, "end": 0.7, "height": 1.9},
                                  {"start": 0.7, "end": 0.9, "height": 0.7}]),
        8: ("staircase", [{"start": 0.05, "end": 0.25, "height": 0.5},
                          {"start": 0.25, "end": 0.45, "height": 0.9},
                          {"start": 0.45, "end": 0.65, "height": 1.4},
                          {"start": 0.65, "end": 0.95, "height": 1.1}]),
        9: ("very_high_central", [{"start": 0.22, "end": 0.78, "height": 1.6}]),
        10: ("high_peak_variant", [{"start": 0.24, "end": 0.76, "height": 1.55}]),
        11: ("pyramid", [{"start": 0.05, "end": 0.20, "height": 0.6},
                         {"start": 0.20, "end": 0.40, "height": 1.4},
                         {"start": 0.40, "end": 0.60, "height": 2.0},
                         {"start": 0.60, "end": 0.80, "height": 1.4},
                         {"start": 0.80, "end": 0.95, "height": 0.6}]),
        12: ("ultra_stretched_pyramid", [{"start": 0.03, "end": 0.18, "height": 0.5},
                                         {"start": 0.18, "end": 0.38, "height": 1.2},
                                         {"start": 0.38, "end": 0.62, "height": 1.9},
                                         {"start": 0.62, "end": 0.82, "height": 1.2},
                                         {"start": 0.82, "end": 0.97, "height": 0.5}]),
        13: ("high_plateau", [{"start": 0.2, "end": 0.8, "height": 1.5}])
    }
    
    pattern = patterns.get(pattern_idx)
    if not pattern:
        return {"error": f"Pattern {pattern_idx} not found"}
    
    name, default_intervals = pattern
    
    mutations = []
    for _ in range(num_variants):
        # Mutate each interval
        mutated_intervals = []
        for interval in default_intervals:
            start = interval["start"] * pos_shift + random.uniform(-0.05, 0.05)
            end = interval["end"] * pos_shift + random.uniform(-0.05, 0.05)
            height = interval["height"] * height_scale + random.uniform(-0.15, 0.15)
            mutated_intervals.append({
                "start": max(0, min(1, start)),
                "end": max(start, min(1, end)),
                "height": max(0.1, height)
            })
        mutations.append({
            "name": name,
            "pattern_idx": pattern_idx,
            "intervals": mutated_intervals,
            "mutation": {"height_scale": height_scale, "pos_shift": pos_shift}
        })
    
    return {
        "type": "pattern_mutation",
        "pattern_idx": pattern_idx,
        "variants": mutations,
        "num_variants": len(mutations)
    }
