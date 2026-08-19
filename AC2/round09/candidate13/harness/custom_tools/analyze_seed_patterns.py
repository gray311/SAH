def run(ctx, args):
    import re, json
    code = ctx.get_program()
    # Extract height patterns from the seed
    heights = []
    widths = []
    for m in re.finditer(r'set\((\d+\.?\d*)\)', code):
        heights.append(float(m.group(1)))
    for m in re.finditer(r'int\((\d+\.?\d*)%\s*\*\s*n\)', code):
        widths.append(float(m.group(1)))
    
    suggestions = []
    if len(heights) >= 3:
        base = sum(heights)/len(heights)
        variations = [
            {'class': 'increased_peaks', 'heights': [h*1.05 if h>=1.5 else h for h in heights]},
            {'class': 'flattened', 'heights': [min(1.8, h*0.95) for h in heights]},
            {'class': 'asymmetric', 'heights': [heights[i]*1.1 if i<3 else heights[i]*0.9 for i in range(len(heights))]}
        ]
        for v in variations:
            suggestions.append(v)
    
    if not suggestions and heights:
        suggestions = [
            {'class': 'shifted', 'heights': heights, 'note': 'same heights, shifted positions'},
            {'class': 'narrowed', 'heights': [h*1.1 for h in heights], 'note': 'narrower widths'},
            {'class': 'widened', 'heights': [h*0.9 for h in heights], 'note': 'wider widths'}
        ]
    
    return {'pattern_class': 'step_functions', 'current_heights': heights[:5], 'suggestions': suggestions[:3]}
