def run(ctx, args):
    import random
    random.seed(42)
    current_best = ctx.get_best_program()
    
    # Parse heights and intervals from code
    lines = current_best.split('\n')
    heights = []
    intervals = []
    
    for line in lines:
        if 'set(' in line:
            h_match = line.split('set(')[1].split(')')[0]
            try:
                heights.append(float(h_match))
            except:
                pass
        
        if 'int(' in line and 'n)' in line:
            i_parts = line.split('int(')
            if len(i_parts) > 1:
                nums = i_parts[1].split(')')[0].split('*')
                if len(nums) >= 2:
                    try:
                        intervals.append((float(nums[0]), float(nums[1])))
                    except:
                        pass
    
    if not heights or not intervals:
        return {"note": "Could not parse pattern, using defaults"}
    
    # Generate 3 variants with different mutation types
    variants = []
    
    # Variant 1: Height perturbation (perturb all heights by small amounts)
    h1 = []
    for h in heights:
        delta = random.uniform(-0.06, 0.06)
        h1.append(round(h + delta, 2))
    variants.append({
        "type": "height_perturbation",
        "description": f"Height perturbation: {heights} → {h1}",
        "code_snippet": current_best + "\n\n# Updated heights: " + str(h1),
        "mutation_params": {"heights": h1, "intervals": intervals}
    })
    
    # Variant 2: Asymmetry induction (make symmetric patterns asymmetric)
    h2 = []
    mid_idx = len(heights) // 2
    for i, h in enumerate(heights):
        if i < mid_idx:
            h2.append(round(h + 0.04, 2))
        elif i == mid_idx:
            h2.append(h)
        else:
            h2.append(round(h - 0.04, 2))
    variants.append({
        "type": "asymmetry",
        "description": f"Asymmetry: {heights} → {h2}",
        "code_snippet": current_best + "\n\n# Asymmetric heights: " + str(h2),
        "mutation_params": {"heights": h2, "intervals": intervals}
    })
    
    # Variant 3: Width adjustment (expand core, contract wings)
    w2 = []
    n_intervals = len(intervals)
    for i, (start, end) in enumerate(intervals):
        if i == 0 or i == n_intervals - 1:
            w2.append((round(start * 0.98, 2), round(end * 0.98, 2)))
        else:
            w2.append((round(start * 1.04, 2), round(end * 1.04, 2)))
    variants.append({
        "type": "width_adjustment",
        "description": f"Width adjustment: {intervals} → {w2}",
        "code_snippet": current_best + "\n\n# Adjusted intervals: " + str(w2),
        "mutation_params": {"heights": heights, "intervals": w2}
    })
    
    return {"variants": variants, "note": "Use probe_solution to rank these 3 variants before full evaluation."}
