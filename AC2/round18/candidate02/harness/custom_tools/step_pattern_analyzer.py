def run(ctx, args):
    import re
    code = ctx.get_program()
    
    heights = []
    positions = []
    widths = []
    
    at_matches = re.findall(r'f\.at\[([^\[\]]+)\]\.(set|replace)\(\s*([\d.]+)\s*\)', code)
    for start_expr, method, value in at_matches:
        heights.append(float(value))
        pos_match = re.search(r'(\d+\.?\d*)\s*\*', start_expr)
        if pos_match:
            positions.append(float(pos_match.group(1)))
        else:
            positions.append(0.5)
    
    num_levels = len(at_matches)
    
    return {
        'num_levels': num_levels,
        'heights': heights,
        'positions': positions,
        'widths': [p * 0.4 for p in positions],
        'note': f'Found {num_levels} level(s) in step pattern'
    }
