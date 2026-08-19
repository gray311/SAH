def run(ctx, args):
    import numpy as np
    from dataclasses import dataclass, asdict
    
    n_intervals = args.get("n_intervals", 100)
    style = args.get("style", "uniform")
    steps = args.get("steps", 3)
    
    N = n_intervals
    domain = 2.0
    dx = domain / N
    h_values = np.zeros(N)
    
    if style == "uniform":
        for i in range(N):
            mid = (i + 0.5) * dx
            if mid < 1.0:
                h_values[i] = 2.0 / N
            else:
                h_values[i] = 0.0
    elif style == "symmetric":
        h_values = np.ones(N) / 2.0
        center = N // 2
        half_width = N // 8
        h_values[center-half_width:center+half_width] = 0.0
        h_values[:half_width] = 1.0
        h_values[N-half_width:N-half_width+half_width] = 1.0
    elif style == "concentrated":
        h_values = np.zeros(N)
        edge_width = N // 6
        h_values[:edge_width] = 3.0 / edge_width
        h_values[N-edge_width:N] = 3.0 / edge_width
    elif style == "multi_step":
        h_values = np.zeros(N)
        segment_width = N // steps
        for step in range(steps):
            center_idx = step * segment_width + segment_width // 2
            amplitude = 1.5 if step < steps // 2 else -0.5
            for i in range(N):
                dist = abs((i + 0.5) * dx - (center_idx + 0.5) * dx)
                h_values[i] += amplitude * np.exp(-dist**2 / (segment_width*dx**2))
    
    h_values = np.clip(h_values, 0.0, 1.0)
    integral = np.sum(h_values) * dx
    if integral > 0:
        h_values = h_values / integral
    
    latent = np.log(h_values / (1.0 - h_values + 1e-10))
    
    class Hyperparameters:
        num_intervals = n_intervals
        base_learning_rate = 0.01
        num_steps = 20000
        penalty_strength = 1000.0
        num_restarts = 1
        seed_start = 42 + int(sum(h_values))
    
    lines = str(ctx.get_best_program()).split('\n')
    new_lines = []
    for i, line in enumerate(lines):
        new_lines.append(line)
        if i == 2 and 'num_intervals' in line:
            new_lines[i] = line.replace('num_intervals = 800', f'num_intervals = {n_intervals}')
        if i == 3 and 'base_learning_rate' in line:
            new_lines[i] = line.replace('0.0053', '0.01')
    
    new_lines.append('')
    new_lines.append(f'    initial_latent = latent')
    new_program = '\n'.join(new_lines)
    
    return {
        "constructed": True,
        "n_intervals": n_intervals,
        "style": style,
        "steps": steps,
        "integral": float(np.sum(h_values) * dx),
        "min_h": float(np.min(h_values)),
        "max_h": float(np.max(h_values)),
        "new_seed_program": new_program,
        "note": f"Constructed {style} step function with {N} intervals"
    }