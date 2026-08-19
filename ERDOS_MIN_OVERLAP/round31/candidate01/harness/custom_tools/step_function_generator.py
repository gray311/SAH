def run(ctx, args):
    import numpy as np
    
    pattern = args.get("pattern_type", "bipartite")
    threshold_or_peaks = args.get("threshold_or_peaks", [])
    n_steps = args.get("n_steps", 4)
    
    N = 1000  # Discretization
    domain = 2.0
    dx = domain / N
    
    h = np.zeros(N)
    
    if pattern == "bipartite":
        # Single threshold: h(x) = 1 for x < a, h(x) = 0 for x >= a
        # integral = a * 1 + (2-a) * 0 = a, so set a=1 for integral=1
        a = 1.0
        for i in range(N):
            x = i * dx
            if x < a:
                h[i] = 1.0
            else:
                h[i] = 0.0
    
    elif pattern == "multi_modal":
        # Multiple peaks with integral=1
        if len(threshold_or_peaks) >= 2:
            peaks = threshold_or_peaks[:min(4, len(threshold_or_peaks))]
            # Create triangular peaks
            for peak_pos in peaks:
                width = 0.3
                for i in range(N):
                    x = i * dx
                    dist = abs(x - peak_pos)
                    if dist < width / 2:
                        h[i] = min(1.0, (width/2 - dist) / (width/2))
            # Normalize to integral=1
            integral = np.sum(h) * dx
            if integral > 0:
                h = h / integral
        else:
            # Fallback to bipartite
            a = 1.0
            for i in range(N):
                x = i * dx
                h[i] = 1.0 if x < a else 0.0
    
    elif pattern == "sparse":
        # Few steps: h(x) = c_i on intervals [t_i, t_{i+1})
        n_intervals = n_steps
        interval_width = 2.0 / n_intervals
        for j in range(n_intervals):
            h[j*n_intervals:(j+1)*n_intervals] = 1.0 / n_intervals
    
    # Ensure h in [0,1] and integral=1
    h = np.clip(h, 0.0, 1.0)
    integral = np.sum(h) * dx
    if abs(integral - 1.0) > 1e-6:
        # Renormalize
        h = h / integral
    
    # Format as Python array string
    h_str = ", ".join([f"{hi:.6f}" for hi in h])
    return {"h": f"array({h_str})", "pattern": pattern, "n_steps": n_steps,
            "integral_check": float(integral)}
