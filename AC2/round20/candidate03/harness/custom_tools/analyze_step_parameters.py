def run(ctx, args):
    best_f = ctx.get_best_program()
    lines = best_f.split('\n')
    params = {'boundaries': [], 'heights': [], 'peak_position': 0.0, 'peak_width': 0.0}
    
    # Parse intervals from the EVOLVE-BLOCK
    in_interval = False
    current_interval = []
    current_height = 0.0
    
    for line in lines:
        if 'start =' in line or 'end =' in line:
            if in_interval:
                params['boundaries'].append(current_interval)
            in_interval = True
            current_interval = []
        if in_interval:
            current_interval.append(line.strip())
            if 'height' in line.lower():
                match = re.search(r'height\s*=\s*([\d.]+)', line, re.IGNORECASE)
                if match:
                    current_height = float(match.group(1))
                    params['heights'].append(current_height)
    
    if in_interval and current_interval:
        params['boundaries'].append(current_interval)
    
    # Estimate peak position and width from heights
    if params['heights']:
        max_height = max(params['heights'])
        peak_indices = [i for i, h in enumerate(params['heights']) if abs(h - max_height) < 0.05]
        params['peak_position'] = len(params['boundaries']) / 2.0
        params['peak_width'] = len(peak_indices) / len(params['boundaries']) if params['boundaries'] else 0.0
    
    params['num_intervals'] = len(params['boundaries']) if params['boundaries'] else 60
    return params
