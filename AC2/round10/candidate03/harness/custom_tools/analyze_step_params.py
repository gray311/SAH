def run(ctx, args):
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"note": "no evolve block", "architectures": []}
    import re
    heights = re.findall(r"\.set\((\d+\.\d+)\)", prog)
    if not heights:
        return {"note": "no step heights found", "current_heights": [], "architectures": []}
    heights = [float(h) for h in heights]
    suggestions = []
    for i, h in enumerate(heights):
        if h > 1.0:
            suggestions.append(f"height[{i}]: try {h*0.95:.3f}, {h*1.05:.3f}")
        else:
            suggestions.append(f"height[{i}]: try {h*0.9:.3f}, {h*1.1:.3f}")
    suggestions = "; ".join(suggestions[:5])
    return {"file": "analyze_step_params", "found_heights": heights,
            "suggested_mutations": suggestions, "architectures": []}
