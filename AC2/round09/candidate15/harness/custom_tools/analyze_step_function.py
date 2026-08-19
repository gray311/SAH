def run(ctx, args):
    import re
    import math
    
    program = ctx.get_program()
    
    # Extract all .set() values (heights)
    height_pattern = r'\.set\(\s*([\d.]+)\s*\)'
    heights = [float(h) for h in re.findall(height_pattern, program)]
    heights = [h for h in heights if h > 0]  # Filter valid heights
    
    # Extract interval fractions
    interval_pattern = r'int\(\s*([\d.]+)\s*[\*\/]\s*(\d+)\s*\)'
    intervals = re.findall(interval_pattern, program)
    
    analysis = {
        "heights_found": heights,
        "num_unique_heights": len(set(heights)),
        "min_height": min(heights) if heights else None,
        "max_height": max(heights) if heights else None,
        "mean_height": sum(heights)/len(heights) if heights else None,
        "max_height_ratio": max(heights)/min(heights) if len(heights) >= 2 and heights[0] > 0 else None,
        "suggestion": "Analyze the pattern"
    }
    
    if not heights:
        analysis["suggestion"] = "No step patterns found - program may be broken or using different approach"
        return analysis
    
    # Give specific mathematical guidance
    max_h = max(heights)
    min_h = min(heights)
    n_heights = len(set(heights))
    
    # Heuristics based on what we know works
    if max_h < 1.7:
        analysis["suggestion"] = f"INCREASE PEAK HEIGHT: Current max={max_h:.2f}. Try increasing to {max_h*1.1:.2f}-{max_h*1.2:.2f}. Higher peaks improve L2 concentration more than L∞."
    elif max_h >= 1.9 and n_heights < 5:
        analysis["suggestion"] = f"ADD MORE LEVELS: Current={n_heights} levels with max={max_h:.2f}. Try adding intermediate levels (e.g., 0.8, 1.9, 2.3, 1.2) to better shape convolution."
    elif n_heights > 6:
        analysis["suggestion"] = f"SIMPLIFY: Too many levels ({n_heights}). Try 3-5 carefully chosen levels. Complexity can dilute the concentration effect."
    elif max_h > 2.0 and min_h < 0.5:
        analysis["suggestion"] = f"REBALANCE HEIGHTS: Very high peak ({max_h:.2f}) with very low base ({min_h:.2f}) may increase L∞ too much. Try raising min to ~0.8."
    else:
        analysis["suggestion"] = f"PATTERNS OK: Heights {min_h:.2f}-{max_h:.2f}, {n_heights} levels. Try asymmetric test: replace middle pattern with 0.8, 2.1, 2.4, 1.1"
    
    return analysis
