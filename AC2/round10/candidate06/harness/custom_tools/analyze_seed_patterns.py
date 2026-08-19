def run(ctx, args):
    prog = ctx.get_program()
    
    # Extract key parameters from the seed program
    import re
    
    result = {
        "analysis": "Analyzing seed step function patterns...",
        "patterns_found": [],
        "suggestions": []
    }
    
    # Find step height patterns like .set(1.42)
    height_matches = re.findall(r'\.set\((\d+\.\d+)\)', prog)
    if height_matches:
        heights = [float(h) for h in height_matches]
        result["found_heights"] = heights
        result["patterns_found"].append({
            "type": "step_heights",
            "values": heights,
            "count": len(heights)
        })
        
        # Suggest refinements
        for h in heights:
            if h > 1.5:
                result["suggestions"].append(
                    f"Consider asymmetric heights: try {h-0.2:.2f} and {h+0.2:.2f} for adjacent steps"
                )
        
    # Find interval patterns
    interval_matches = re.findall(r'int\(int\((\d+\.\d+).*?/.*?\.set', prog)
    
    # Check for symmetry
    if height_matches:
        mid_idx = len(height_matches) // 2
        left_half = height_matches[:mid_idx]
        right_half = height_matches[mid_idx:]
        if abs(float(left_half[-1]) - float(right_half[0])) < 0.01:
            result["patterns_found"].append({
                "type": "symmetric",
                "note": "Detected symmetric pattern around center"
            })
        else:
            result["patterns_found"].append({
                "type": "asymmetric_potential",
                "note": "Consider asymmetric variants"
            })
    
    # Suggest structural changes
    result["suggestions"].extend([
        "Try asymmetric step patterns (different left/right heights)",
        "Test plateau variants with sloped transitions",
        "Explore multi-level steps with 4-5 height levels",
        "Consider narrowing the central peak while extending wings",
        "Test polynomial smoothing at step boundaries"
    ])
    
    result["recommendation"] = (
        f"Start with {len(height_matches)}-height asymmetric variants, then"
        " probe 3-5 variants before full evaluation."
    )
    
    return result
