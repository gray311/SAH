def run(ctx, args):
    import numpy as np
    config = args
    # Get num_intervals from the seed program
    prog = ctx.get_program()
    num_intervals_line = [line for line in prog.split('\n') if 'num_intervals:' in line]
    n = 350  # default from seed
    if num_intervals_line:
        try:
            n = int(num_intervals_line[0].split(' = ')[1].strip())
        except:
            pass
    
    # Generate step configuration
    num_steps = config.get("num_steps", int(np.random.uniform(2, 6)))
    symmetric = config.get("symmetric", True)
    min_h = config.get("height_range", {}).get("min", 0.8)
    max_h = config.get("height_range", {}).get("max", 2.0)
    
    # Generate step intervals
    step_widths = np.random.uniform(0.15, 0.25, num_steps)
    centers = np.zeros(num_steps)
    heights = np.random.uniform(min_h, max_h, num_steps)
    
    if symmetric:
        # Symmetric around 0
        centers[0] = 0.0
        half_width = np.random.uniform(0.3, 0.5)
        centers[1] = half_width
        centers[2] = -half_width
        centers = centers[centers != 0]
    else:
        # Asymmetric: random centers
        centers = np.random.uniform(-0.4, 0.4, num_steps)
    
    # Create step function as numpy array
    f = np.zeros(n)
    for c, sw, h in zip(centers, step_widths, heights):
        left = int((c - sw) * n)
        right = int((c + sw) * n)
        f[left:right] = h
    
    return {
        "type": "step_function",
        "num_steps": num_steps,
        "symmetric": symmetric,
        "centers": centers.tolist(),
        "widths": step_widths.tolist(),
        "heights": heights.tolist(),
        "array_preview": f[:10].tolist(),
        "instructions": f"Replace num_intervals={n} and create step function with {num_steps} steps at centers={centers.tolist()}, widths={step_widths.tolist()}, heights={heights.tolist()}"
    }
