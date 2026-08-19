def run(ctx, args):
    import random, re
    variety = args.get("variety", "diverse")
    num_patterns = args.get("num_patterns", 70)
    min_int = args.get("min_intervals", 300)
    max_int = args.get("max_intervals", 800)
    
    # Extract the seed program's pattern creation logic
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"note": "no evolve block", "patterns": []}
    
    # Pattern class definitions (pattern: (name, heights_list, starts_list, ends_list))
    pattern_defs = [
        ("single_peak", [1.5], [0.25], [0.75]),
        ("multi_3peak", [0.9, 1.8, 0.9], [0.15, 0.25], [0.25, 0.40, 0.70, 0.85]),
        ("plateau", [1.4], [0.20], [0.80]),
        ("staircase_4", [0.7, 1.2, 1.7, 1.0], [0.06, 0.20, 0.35, 0.64], [0.20, 0.35, 0.64, 0.94]),
        ("asymmetric_3", [0.8, 2.0, 0.8], [0.12, 0.28], [0.28, 0.50, 0.80, 0.88]),
        ("pyramid_5", [0.7, 1.5, 2.1, 1.5, 0.7], [0.06, 0.19, 0.40, 0.60, 0.80], [0.19, 0.40, 0.60, 0.80, 0.94]),
        ("winged", [0.8, 2.0, 0.8], [0.15, 0.30], [0.30, 0.50, 0.70, 0.85]),
        ("tall_narrow", [2.2], [0.22], [0.78]),
        ("bimodal", [1.0, 1.9, 1.0], [0.20, 0.40], [0.40, 0.55, 0.75, 0.80]),
    ]
    
    codes = []
    for _ in range(num_patterns):
        n_intervals = random.randint(min_int, max_int)
        choice_idx = random.randint(0, len(pattern_defs) - 1)
        name, heights, starts, ends = pattern_defs[choice_idx]
        
        # Build code to create this pattern using jax
        lines = ['# Pattern: {} (intervals: {})'.format(name, n_intervals)]
        lines.append('f = jnp.zeros({})'.format(n_intervals))
        for i, (start, end, h) in enumerate(zip(starts, ends, heights)):
            s_idx = int(start * n_intervals)
            e_idx = int(end * n_intervals)
            lines.append('f = f.at[{}:{}.].set({:.2f})'.format(s_idx, e_idx, h))
        codes.append('\n'.join(lines))
    
    return {
        "num_patterns_generated": len(codes),
        "variety": variety,
        "patterns": codes,
        "note": "Copy pattern code into EVOLVE-BLOCK and run probe/evaluate on them."
    }
