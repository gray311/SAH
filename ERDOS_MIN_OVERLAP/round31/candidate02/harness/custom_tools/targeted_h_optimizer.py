def run(ctx, args):
    h_text = ctx.get_best_program()
    if not h_text:
        return {"error": "No h array"}
    
    import re
    patterns = [
        r"h\s*=\s*array\s*\(([^)]+)\)",
        r"h\s*=\s*np\.array\s*\(([^)]+)\)"
    ]
    match = None
    for p in patterns:
        m = re.search(p, h_text, re.IGNORECASE)
        if m:
            match = m
            break
    
    if not match:
        return {"error": "Could not parse h array"}
    
    try:
        h_vals = np.array([float(x.strip()) for x in match.group(1).split(",")])
    except:
        return {"error": "Failed to parse h values"}
    
    N = len(h_vals)
    dx = 2.0 / N
    
    strategy = args.get("strategy", "spread_peaks")
    problematic_k = args.get("problematic_k", [])
    
    # Strategy: spread_peaks - create multiple narrow peaks
    if strategy == "spread_peaks":
        num_peaks = 3
        peak_positions = np.linspace(0.2, 1.8, num_peaks)
        peak_widths = 0.08
        
        new_h = np.zeros(N)
        for i, pos in enumerate(peak_positions):
            peak_idx = int(pos / dx)
            width_idx = int(peak_widths / dx)
            new_h[peak_idx-width_idx:peak_idx+width_idx+1] = 1.0 / (2*width_idx+1)
        
        # Ensure integral = 1
        current_int = np.sum(new_h) * dx
        scale = 1.0 / current_int
        new_h = new_h * scale
        
    # Strategy: asymmetric - different thresholds left and right of x=1
    elif strategy == "asymmetric":
        left_threshold = 0.3
        right_threshold = 0.7
        
        new_h = np.zeros(N)
        for i in range(N):
            x = i * dx
            if x < 1.0:
                new_h[i] = left_threshold
            else:
                new_h[i] = right_threshold
        
        # Ensure integral = 1
        current_int = np.sum(new_h) * dx
        scale = 1.0 / current_int
        new_h = new_h * scale
        
    # Strategy: bimodal - two distinct peaks
    elif strategy == "bimodal":
        peak1_pos = 0.4
        peak2_pos = 1.4
        peak_width = 0.12
        
        new_h = np.zeros(N)
        for i, pos in enumerate([peak1_pos, peak2_pos]):
            peak_idx = int(pos / dx)
            width_idx = int(peak_width / dx)
            new_h[peak_idx-width_idx:peak_idx+width_idx+1] = 1.0 / (2*width_idx+1)
        
        current_int = np.sum(new_h) * dx
        scale = 1.0 / current_int
        new_h = new_h * scale
    
    # Generate mutation by perturbing original h
    new_h_muted = h_vals + np.random.normal(0, 0.05, N)
    new_h_muted = np.clip(new_h_muted, 0.01, 0.99)
    
    # Reconstruct with strategy-based structure
    if strategy == "spread_peaks":
        for pos in peak_positions:
            peak_idx = int(pos / dx)
            width_idx = int(peak_widths / dx)
            new_h_muted[peak_idx-width_idx:peak_idx+width_idx+1] = 0.6
    
    current_int = np.sum(new_h_muted) * dx
    scale = 1.0 / current_int
    new_h_muted = np.clip(new_h_muted * scale, 0.01, 0.99)
    
    # Generate new h array string
    new_h_str = ", ".join([f"{v:.6f}" for v in new_h_muted])
    
    return {
        "new_h": f"array({new_h_str})",
        "strategy_used": strategy,
        "note": f"Generated {strategy} mutation"
    }
