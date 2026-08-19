def run(ctx, args):
    import numpy as np
    program = ctx.get_program()
    parts = program.split('num_intervals')
    if len(parts) < 2:
        num_intervals = 100
    else:
        val = parts[1].split('=')
        if len(val) < 2:
            num_intervals = 100
        else:
            num_intervals = int(val[1].strip().split('\n')[0])
    
    if num_intervals < 50:
        num_intervals = 100
    x = np.linspace(0, 2, num_intervals + 1)
    dx = 2.0 / num_intervals
    num_candidates = 5
    candidates = []
    
    # Candidate 1: Single symmetric bump
    candidates.append({
        'name': 'single_bump',
        'breakpoints': [0.5, 1.5],
        'heights': [1.0],
        'h_values': np.zeros(num_intervals)
    })
    c = candidates[-1]
    left_w, right_w = 0.5/2.0, 0.5/2.0
    if left_w > dx:
        start = int(0.5/2.0/dx)
        end = start + int(1.0/2.0/dx)
        if end <= num_intervals:
            c['h_values'][start:end] = 1.0
    
    # Candidate 2: Two symmetric bumps
    candidates.append({
        'name': 'two_bumps',
        'breakpoints': [0.25, 0.75, 1.25, 1.75],
        'heights': [0.5, 0.5],
        'h_values': np.zeros(num_intervals)
    })
    c = candidates[-1]
    start1 = int(0.25/dx)
    end1 = int(0.75/dx)
    if end1 <= num_intervals:
        c['h_values'][start1:end1] = 0.5
    start2 = int(1.25/dx)
    end2 = int(1.75/dx)
    if end2 <= num_intervals:
        c['h_values'][start2:end2] = 0.5
    
    # Candidate 3: Concentrated center mass
    candidates.append({
        'name': 'center_concentrated',
        'breakpoints': [0.8, 1.2],
        'heights': [1.25, 1.25],
        'h_values': np.zeros(num_intervals)
    })
    c = candidates[-1]
    start = int(0.8/dx)
    end = int(1.2/dx)
    if end <= num_intervals:
        c['h_values'][start:end] = 1.25
    
    # Candidate 4: Left-heavy
    candidates.append({
        'name': 'left_heavy',
        'breakpoints': [0.4, 1.6],
        'heights': [1.5, 0.25],
        'h_values': np.zeros(num_intervals)
    })
    c = candidates[-1]
    start = int(0.4/dx)
    end = int(1.6/dx)
    if end <= num_intervals:
        c['h_values'][start:end] = 1.5
    if end < num_intervals:
        c['h_values'][end:] = 0.25
    
    # Candidate 5: Threshold with decay
    candidates.append({
        'name': 'threshold_decay',
        'breakpoints': [0.0, 0.5, 1.0, 2.0],
        'heights': [1.0, 0.5, 0.0],
        'h_values': np.zeros(num_intervals)
    })
    c = candidates[-1]
    end1 = int(0.5/dx)
    if end1 <= num_intervals:
        c['h_values'][:end1] = 1.0
    end2 = int(1.0/dx)
    if end2 <= num_intervals:
        c['h_values'][end1:end2] = 0.5
    
    results = []
    for c in candidates:
        # Normalize to integral=1
        integral = np.sum(c['h_values']) * dx
        if integral > 0:
            c['h_values'] = c['h_values'] * (1.0 / integral)
            c['h_values'] = np.clip(c['h_values'], 0, 1)
        results.append(c)
    
    return {"candidates": results, "num_intervals": num_intervals}