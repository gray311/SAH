def run(ctx, args):
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"note": "no evolve block"}
    import re
    int_match = re.search(r'num_intervals:\s*(\d+)', prog)
    num_intervals = int(int_match.group(1)) if int_match else 450
    
    heights = re.findall(r'\.set\((\d+\.?\d*)\)', prog)
    heights = [float(h) for h in heights if h.strip()]
    
    ranges = re.findall(r'\.at\s*\(\s*int\s*\(\s*([\d.]+)\s*\*\s*(\w+)\s*\)\s*:\s*int\s*\(\s*([\d.]+)\s*\*\s*(\w+)\s*\)\s*\)', prog)
    
    analysis = {
        "num_intervals": num_intervals,
        "num_heights": len(heights),
        "heights": heights,
        "avg_height": sum(heights)/len(heights) if heights else 0,
        "max_height": max(heights) if heights else 0,
        "min_height": min(heights) if heights else 0,
        "suggestion": "Test asymmetric splits, varying resolutions (300-900), and multi-peak architectures"
    }
    return analysis
