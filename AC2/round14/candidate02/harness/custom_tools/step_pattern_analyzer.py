def run(ctx, args):
    import re
    program = ctx.get_program()
    heights = re.findall(r'base_height\s*=\s*([\d.]+)', program)
    heights = [float(h) for h in heights] if heights else []
    width_patterns = re.findall(r'int\(([0-9.]+)\s*\*\s*n\)', program)
    widths = [float(w) for w in width_patterns] if width_patterns else []
    bump_heights = re.findall(r'bump(\d*)_height\s*=\s*([\d.]+)', program)
    for _, bh in bump_heights:
        heights.append(float(bh))
    width_ratios = []
    if len(widths) >= 2:
        for i in range(len(widths)-1):
            width_ratios.append(widths[i+1]/max(widths[i], 1e-6))
    asymmetry = 0.0
    if len(widths) >= 4:
        left_width = sum(widths[:len(widths)//2])
        right_width = sum(widths[len(widths)//2:])
        asymmetry = abs(left_width - right_width) / max(left_width + right_width, 1e-6)
    suggestions = []
    if heights:
        max_h_idx = heights.index(max(heights))
        min_h_idx = heights.index(min(heights))
        suggestions.append({"type": "height_increase", "target": f"height_{max_h_idx}", "direction": "increase", "magnitude": 0.05, "rationale": "Increase tallest level to boost L2 norm more than infinity norm"})
        suggestions.append({"type": "height_decrease", "target": f"height_{min_h_idx}", "direction": "decrease", "magnitude": 0.05, "rationale": "Decrease shortest level to reduce infinity norm"})
    if width_ratios:
        avg_ratio = sum(width_ratios) / len(width_ratios)
        for i, ratio in enumerate(width_ratios):
            if ratio > avg_ratio * 1.1:
                suggestions.append({"type": "width_contract", "target": f"width_{i}", "direction": "contract", "magnitude": 0.05, "rationale": "Contract wide interval to reduce ||f★f||_∞"})
            elif ratio < avg_ratio * 0.9:
                suggestions.append({"type": "width_expand", "target": f"width_{i}", "direction": "expand", "magnitude": 0.05, "rationale": "Expand narrow interval to boost ||f★f||₂²"})
    while len(suggestions) < 3:
        suggestions.append({"type": "height_perturb", "target": "random_level", "direction": "random_pm_0.03", "magnitude": 0.03, "rationale": "Small random perturbation to explore local neighborhood"})
    return {"num_levels": len(heights), "heights": heights[:10], "width_ratios": width_ratios[:5], "asymmetry": asymmetry, "suggestions": suggestions[:5]}
