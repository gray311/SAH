def run(ctx, args):
    import re
    prog = ctx.get_program()
    
    heights_all = re.findall(r'\.set\((\d+\.\d+)\)', prog)
    heights_all = [float(h) for h in heights_all if h]
    
    positions = re.findall(r'int\((\d+\.\d+)\*n\)', prog)
    positions = [float(p) for p in positions]
    
    unique_heights = sorted(set([round(h, 2) for h in heights_all]))
    
    return {
        "total_heights_found": len(heights_all),
        "unique_heights": unique_heights,
        "base_intervals": positions[:20],
        "recommendation": "Use these heights as mutation targets. Try small variations (±5-10%).",
        "note": "The current best is likely one of the multi-level patterns (3-5 levels). Mutate the tallest peak first."
    }
