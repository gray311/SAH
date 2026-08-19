def run(ctx, args):
    import re
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"error": "no evolve block", "heights": [], "n_patterns": 0}

    # Extract all heights from f.at[...].set(H) patterns
    heights = re.findall(r'\.set\((\d+\.\d+)\)', prog)
    heights = [float(h) for h in heights if h]

    # Basic statistics
    if not heights:
        return {"error": "no heights found", "heights": [], "n_patterns": 0}
    
    max_h = max(heights)
    min_h = min(heights)
    avg_h = sum(heights) / len(heights)
    h_range = max_h - min_h
    height_std = (sum((h - avg_h)**2 for h in heights) / len(heights)) ** 0.5

    # Determine symmetry
    is_symmetric = abs(max_h - min_h) < 0.1 * max_h if max_h > 0 else True

    # Count unique height levels
    unique_heights = sorted(set(round(h, 1) for h in heights))
    n_levels = len(unique_heights)

    return {
        "analysis": {
            "height_range": h_range,
            "avg_height": avg_h,
            "max_height": max_h,
            "min_height": min_h,
            "height_std": height_std,
            "n_unique_levels": n_levels,
            "is_symmetric": is_symmetric
        },
        "heights": heights,
        "suggested_improvements": [
            f"Consider asymmetric patterns breaking symmetry (current is_symmetric={is_symmetric})",
            f"Explore {n_levels + 1}-level patterns for increased complexity",
            "Try smooth transitions between current discrete levels",
            "Experiment with irregular spacing of current intervals"
        ]
    }