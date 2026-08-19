def run(ctx, args):
    import re
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"note": "no evolve block", "proposals": []}
    
    # Extract all height values and their contexts from patterns like f.at[...].set(1.42)
    height_matches = re.findall(r'\\.set\\((\\d+\\.\\d+)\\)', prog)
    height_matches += re.findall(r'set\\((\\d+\\.\\d+)\\)', prog)  # Alternative format
    heights = [float(h) for h in height_matches if h and h.replace('.','').isdigit() or re.match(r'^\\d+\\.\\d+$', h)]
    
    if not heights:
        return {"note": "could not parse heights", "proposals": []}
    
    # Analyze pattern characteristics
    avg_h = sum(heights) / len(heights)
    std_h = (sum((h - avg_h)**2 for h in heights) / len(heights)) ** 0.5
    min_h = min(heights)
    max_h = max(heights)
    h_range = max_h - min_h
    h_variance = std_h / avg_h if avg_h > 0 else 0
    
    # Categorize current pattern
    num_levels = len(heights)
    pattern_type = "unknown"
    if h_range < 0.1:
        pattern_type = "nearly_uniform"
    elif h_range < 0.3:
        pattern_type = "moderate_variation"
    else:
        pattern_type = "high_variation"
    
    # Generate mutation proposals
    proposals = []
    
    # Proposal 1: Height perturbation (increase one peak, decrease others)
    peak_idx = heights.index(max_h) if heights else 0
    proposals.append({
        "mutation_type": "height_perturbation",
        "description": "Increase main peak by 0.08, decrease others by 0.04 to optimize L2/∞ ratio",
        "changes": {
            "peak_increase": 0.08,
            "others_decrease": 0.04,
            "target_indices": [peak_idx],
            "affected_count": 1
        },
        "rationale": "Higher peak increases ||f★f||₂²; decreasing side peaks reduces potential ||f★f||∞ spikes"
    })
    
    # Proposal 2: Width expansion on core interval
    proposals.append({
        "mutation_type": "width_expansion",
        "description": "Expand the central interval by 8% to increase convolution support",
        "changes": {
            "target": "central_interval",
            "expansion_fraction": 0.08,
            "expected_effect": "increases_L2_norm"
        },
        "rationale": "Wider core increases overlap region in convolution, boosting L2 norm without necessarily increasing infinity norm"
    })
    
    # Proposal 3: Center of mass shift
    proposals.append({
        "mutation_type": "center_shift",
        "description": "Shift all interval boundaries right by 0.02 (2% of domain)",
        "changes": {
            "shift_direction": "right",
            "shift_fraction": 0.02,
            "all_intervals": True
        },
        "rationale": "Breaking perfect symmetry can reduce constructive interference at certain points, lowering ||f★f||∞"
    })
    
    # Proposal 4: Asymmetric height variation
    if pattern_type in ["moderate_variation", "high_variation"]:
        proposals.append({
            "mutation_type": "asymmetric_variation",
            "description": "Make heights asymmetric: apply +6% to some, -4% to others",
            "changes": {
                "asymmetry_direction": "alternating",
                "perturbation_positive": 0.06,
                "perturbation_negative": -0.04,
                "apply_to": "all_levels_alternating"
            },
            "rationale": "Asymmetric patterns break exact symmetry, potentially reducing ||f★f||∞ while maintaining ||f★f||₂²"
        })
    
    # Proposal 5: Intermediate level adjustment (for multi-level patterns)
    if num_levels >= 4:
        proposals.append({
            "mutation_type": "intermediate_adjustment",
            "description": "Increase intermediate levels by 0.05, keep core peaks unchanged",
            "changes": {
                "target": "intermediate_levels",
                "increase_amount": 0.05,
                "preserve": "main_peaks"
            },
            "rationale": "Higher intermediate levels increase convolution support without dominating the infinity norm"
        })
    
    return {
        "analysis": {
            "num_levels": num_levels,
            "avg_height": avg_h,
            "height_range": h_range,
            "pattern_type": pattern_type,
            "std_dev_ratio": h_variance
        },
        "proposals": proposals
    }
