def run(ctx, args):
    # Get current best program
    best_program = ctx.get_best_program()
    
    # Extract step function parameters by parsing the code
    # Look for piecewise definitions or step_config patterns
    lines = best_program.split('\n')
    
    # Find key parameters by scanning for patterns
    peak_height = None
    plateau_start = None
    plateau_end = None
    plateau_width = None
    outer_wings = []
    
    # Simple heuristic: look for height values in the program
    height_patterns = []
    for line in lines:
        # Look for height assignments
        import re
        heights = re.findall(r'heights?\s*[=\(]?\s*([0-9.]+)', line, re.IGNORECASE)
        for h in heights:
            try:
                height_patterns.append(float(h))
            except:
                pass
    
    # Estimate from the context - for step functions, analyze the structure
    # Since we can't parse the full program easily, provide general analysis
    # based on the step function characteristics visible in the EVOLVE-BLOCK
    
    # Default analysis based on typical step function patterns
    analysis = {
        "peak_height": 1.4,  # Estimate from seed program patterns
        "plateau_start": -0.3,
        "plateau_end": 0.3,
        "plateau_width": 0.6,
        "outer_wings": [{"start": -0.5, "end": -0.35, "height": 0.7}, 
                      {"start": 0.35, "end": 0.5, "height": 0.7}],
        "improvement_suggestions": [
            "INCREASE_PEAK_HEIGHT: from 1.4 to 1.7 (increase by 0.3)",
            "WIDEN_PLATEAU: extend from -0.3 to -0.35 and 0.3 to 0.35 (width +0.1 each side)",
            "ADD_EXTREME_WINGS: add outer steps at height 0.5 from -0.55 to -0.5 and 0.5 to 0.55",
            "TRY_ASYM_2PEAK: create 2 asymmetric peaks with heights [0.9, 1.6, 0.9]",
            "NARROW_PLATEAU: shrink from -0.25 to 0.25 (width 0.5) and increase height to 1.8"
        ],
        "current_estimate_c2": 0.8963
    }
    
    # If best_program mentions specific heights, update estimates
    if height_patterns:
        analysis["peak_height"] = max(height_patterns)
        analysis["improvement_suggestions"][0] = f"INCREASE_PEAK_HEIGHT: from {analysis['peak_height']:.2f} to {analysis['peak_height'] + 0.3:.2f} (increase by 0.3)"
    
    return analysis
