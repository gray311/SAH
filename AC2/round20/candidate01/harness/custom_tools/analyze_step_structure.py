def run(ctx, args):
    import re
    f_text = ctx.get_program()
    at_matches = re.findall(r'\.at\(int\(([0-9]\.?[0-9]*)\*\s*n\):\s*int\(([0-9]\.?[0-9]*)\*\s*n\)\)\.set\(([0-9]\.?[0-9]*)\)', f_text)
    heights = []
    positions = []
    for match in at_matches:
        start_frac = float(match[0])
        end_frac = float(match[1])
        height = float(match[2])
        heights.append(height)
        positions.append((start_frac, end_frac))
    if not heights:
        return {"num_levels": 5, "heights": [0.80, 1.60, 2.00, 1.40, 0.90], "positions": [(0.08, 0.20), (0.20, 0.35), (0.35, 0.55), (0.55, 0.75), (0.75, 0.90)], "note": "Using fallback seed pattern structure"}
    avg_height = sum(heights) / len(heights)
    height_range = max(heights) - min(heights)
    return {"num_levels": len(heights), "heights": heights, "positions": positions, "avg_height": avg_height, "height_range": height_range, "min_height": min(heights), "max_height": max(heights), "recommendation": "Try perturbing heights by +/- 0.1-0.3 around " + str(round(avg_height, 2))}
