def run(ctx, args):
    import re
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"note": "no evolve block"}
    
    # Extract heights from patterns like f.at[...].set(1.42)
    heights = re.findall(r'\.set\((\d+\.\d+)\)', prog)
    heights = [float(h) for h in heights if h]
    
    if not heights:
        return {"note": "could not parse heights", "proposals": []}
    
    # Analyze current pattern characteristics
    max_h = max(heights)
    min_h = min(heights)
    h_range = max_h - min_h
    avg_h = sum(heights) / len(heights)
    
    # Generate diverse new pattern proposals
    proposals = []
    
    # Proposal 1: Asymmetric three-peak pattern
    if h_range > 0.1:
        proposals.append({
            "name": "asymmetric_3peak",
            "description": "Three peaks with unequal heights and positions to break symmetry",
            "heights": [min_h * 0.7, max_h * 1.35, min_h * 0.9, max_h * 1.1, min_h * 0.6],
            "rationale": "Asymmetry in peak structure may reduce ||f★f||∞ while maintaining ||f★f||₂²"
        })
    
    # Proposal 2: Smooth transition pattern (mimicking spline behavior)
    proposals.append({
        "name": "smooth_transition",
        "description": "Step pattern with gradual transitions using exponential-like behavior",
        "heights": [avg_h * 1.2, avg_h * 0.8, avg_h * 1.4, avg_h * 0.6, avg_h * 1.1],
        "rationale": "Smoother transitions in convolution may improve L2 norm without increasing infinity norm"
    })
    
    # Proposal 3: Irregular multi-level pattern
    proposals.append({
        "name": "irregular_multi",
        "description": "Irregularly spaced multi-level steps with varying widths",
        "heights": [max_h * 0.8, max_h * 1.45, avg_h * 0.7, max_h * 1.25, avg_h * 0.9],
        "rationale": "Irregular spacing may avoid constructive interference in convolution peaks"
    })
    
    # Proposal 4: Centered asymmetric pattern
    if len(heights) >= 3:
        proposals.append({
            "name": "centered_asymmetric",
            "description": "Central peak dominates with asymmetric side peaks",
            "heights": [avg_h * 0.6, max_h * 1.55, avg_h * 0.5, max_h * 1.3, avg_h * 0.4],
            "rationale": "Dominant central peak with smaller asymmetric wings may optimize the ratio"
        })
    
    # Proposal 5: Staircase variant
    proposals.append({
        "name": "staircase_asymmetric",
        "description": "Asymmetric staircase with increasing/decreasing steps",
        "heights": [avg_h * 0.75, avg_h * 0.85, avg_h * 0.95, avg_h * 1.1, avg_h * 1.25, avg_h * 1.0],
        "rationale": "Monotonic (or near-monotonic) step structure may improve convolution properties"
    })
    
    return {
        "analysis": {
            "height_range": h_range,
            "avg_height": avg_h,
            "max_height": max_h,
            "current_proposals_count": len(heights)
        },
        "proposals": proposals
    }
