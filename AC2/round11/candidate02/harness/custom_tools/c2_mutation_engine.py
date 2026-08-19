def run(ctx, args):
    import re
    prog = ctx.get_program()
    
    if "# EVOLVE-BLOCK" not in prog:
        return {"error": "no evolve block", "proposals": []}
    
    # Extract all actual numerical height values from the program
    # Pattern: .set(NUMBER) where NUMBER is like 1.40, 2.30, etc.
    heights = re.findall(r'\.set\((\d+\.\d+)\)', prog)
    heights = [float(h) for h in heights if h]
    
    if len(heights) < 3:
        return {"error": "could not parse sufficient heights", "proposals": []}
    
    # Analyze current pattern characteristics
    max_h = max(heights)
    min_h = min(heights)
    avg_h = sum(heights) / len(heights)
    h_std = (sum((h - avg_h)**2 for h in heights) / len(heights)) ** 0.5
    
    proposals = []
    
    # Proposal 1: Amplified asymmetry - increase contrast between peaks
    prop1_heights = [avg_h * 0.55, max_h * 1.60, avg_h * 0.40, max_h * 1.40, avg_h * 0.30]
    proposals.append({
        "name": "amplified_asymmetry",
        "description": "Extreme asymmetry with very high central peak and small wings",
        "heights": prop1_heights,
        "rationale": f"Increasing height contrast (max: {max_h:.2f}, min: {min_h:.2f}) to reduce convolution infinity norm",
        "concrete_values": prop1_heights
    })
    
    # Proposal 2: Broaden the peak distribution - wider spread
    num_levels = min(13, len(heights))
    center_idx = num_levels // 2
    prop2_heights = []
    for i in range(num_levels):
        if i == center_idx:
            prop2_heights.append(max_h * 1.55)
        elif i == center_idx - 1 or i == center_idx + 1:
            prop2_heights.append(avg_h * 1.25)
        else:
            prop2_heights.append(avg_h * 0.65)
    proposals.append({
        "name": "broadened_distribution",
        "description": "Broader peak distribution with smoother height transitions",
        "heights": prop2_heights,
        "rationale": "Spreading mass across more levels may improve the L2 to infinity ratio",
        "concrete_values": prop2_heights
    })
    
    # Proposal 3: Multiple small peaks (anti-constructive interference)
    prop3_heights = [avg_h * 1.3, avg_h * 0.7, avg_h * 1.45, avg_h * 0.6, avg_h * 1.35, avg_h * 0.75]
    proposals.append({
        "name": "multiple_small_peaks",
        "description": "Multiple moderate peaks instead of one dominant peak",
        "heights": prop3_heights,
        "rationale": "Distributed peaks may avoid constructive interference at convolution infinity",
        "concrete_values": prop3_heights
    })
    
    # Proposal 4: Steep central peak with gradual wings
    prop4_heights = [avg_h * 0.75, avg_h * 1.3, max_h * 1.70, avg_h * 0.95, avg_h * 0.80]
    proposals.append({
        "name": "steep_peak_gentle_wings",
        "description": "Sharp central peak with gradually tapering wings",
        "heights": prop4_heights,
        "rationale": f"Concentrating mass centrally (max_h: {max_h:.2f}) while softening edges",
        "concrete_values": prop4_heights
    })
    
    # Proposal 5: Offset pyramid - asymmetric pyramid structure
    if len(heights) >= 5:
        prop5_heights = [avg_h * 0.60, avg_h * 1.20, max_h * 1.45, avg_h * 0.90, avg_h * 0.55]
        proposals.append({
            "name": "offset_pyramid",
            "description": "Asymmetric pyramid with the tallest peak offset to the left",
            "heights": prop5_heights,
            "rationale": "Offset peak structure may exploit convolution asymmetry",
            "concrete_values": prop5_heights
        })
    
    # Proposal 6: Very high narrow peak strategy
    prop6_heights = [avg_h * 0.50, avg_h * 0.85, max_h * 1.95, avg_h * 0.70, avg_h * 0.55]
    proposals.append({
        "name": "narrow_high_peak",
        "description": "Very tall narrow central peak with minimal wings",
        "heights": prop6_heights,
        "rationale": f"Extremely high peak (target: ~{max_h * 1.95:.2f}) to maximize L2 contribution",
        "concrete_values": prop6_heights
    })
    
    # Summary stats
    return {
        "analysis": {
            "height_range": max_h - min_h,
            "avg_height": avg_h,
            "max_height": max_h,
            "min_height": min_h,
            "std_dev": h_std,
            "current_heights_count": len(heights)
        },
        "num_proposals": len(proposals),
        "proposals": proposals
    }
