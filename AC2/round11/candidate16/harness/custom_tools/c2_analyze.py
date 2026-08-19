def run(ctx, args):
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"error": "no evolve block"}
    
    import re
    heights = re.findall(r'\.set\((\d+\.\d+)\)', prog)
    heights = [float(h) for h in heights if h]
    
    if not heights:
        return {"note": "Could not parse pattern heights", "heights": []}
    
    max_h = max(heights)
    min_h = min(heights)
    avg_h = sum(heights) / len(heights)
    
    return {
        "height_range": max_h - min_h,
        "avg_height": avg_h,
        "max_height": max_h,
        "min_height": min_h,
        "num_heights": len(heights),
        "note": "Use c2_analyze output to guide further mutations. Call evaluate_solution only if analysis shows potential."
    }
