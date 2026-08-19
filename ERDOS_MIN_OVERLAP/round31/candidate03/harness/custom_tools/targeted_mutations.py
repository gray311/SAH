def run(ctx, args):
    import numpy as np
    import re
    
    # Get current h array
    h_str = ctx.get_best_program()
    if h_str is None or h_str == "":
        return {"error": "No best program available"}
    
    patterns = [
        r"'\s*=.*array\s*\(([^)]+)",
        r'h\s*=.*array\s*\(([^)]+)',
        r'h\s*=.*np\.array\s*\(([^)]+)'
    ]
    
    match = None
    for pattern in patterns:
        m = re.search(pattern, h_str, re.IGNORECASE)
        if m:
            match = m
            break
    
    if not match:
        return {"error": "Could not parse h array"}
    
    try:
        h_vals = np.array([float(x.strip()) for x in match.group(1).split(",")])
    except Exception as e:
        return {"error": "Failed to parse h values: " + str(e)}
    
    N = len(h_vals)
    domain = 2.0
    dx = domain / N
    
    # Get mutation parameters
    mutation_type = args.get("mutation_type", "bipartite")
    step_width = args.get("step_width", 0.1)
    peak_height = args.get("peak_height", 0.8)
    
    # Generate mutation based on type
    if mutation_type == "bipartite":
        # Create bipartite: h=1 over [0, 2] (full domain)
        new_h = np.ones(N)
        # Normalize to integral=1
        current_integral = np.trapz(new_h, dx=dx)
        if current_integral > 0:
            new_h = new_h / (current_integral / dx)
        new_h = np.clip(new_h, 0.0, 1.0)
    
    elif mutation_type == "tri-modal":
        # Three narrow peaks
        centers = [0.33, 1.0, 1.66]
        new_h = np.zeros(N)
        for center in centers:
            center_idx = int(center / dx)
            width = int(step_width / dx)
            if width > 0:
                new_h[center_idx: min(center_idx + width, N)] = peak_height
        
        # Normalize to integral=1
        current_integral = np.trapz(new_h, dx=dx)
        if current_integral > 0:
            new_h = new_h / (current_integral / dx)
        new_h = np.clip(new_h, 0.0, 1.0)
    
    else:  # uniform-noise
        np.random.seed(int(N * dx * 12345))
        new_h = h_vals + np.random.normal(0, step_width, N)
        new_h = np.clip(new_h, 0.0, 1.0)
        # Normalize to integral=1
        current_integral = np.trapz(new_h, dx=dx)
        if current_integral > 0:
            new_h = new_h / (current_integral / dx)
    
    # Format as string
    h_new = "h = np.array(" + ", ".join([f"{x:.6f}" for x in new_h]) + ")"
    
    return {
        "mutation_type": mutation_type,
        "new_h": h_new,
        "integral_check": float(np.trapz(new_h, dx=dx))
    }
