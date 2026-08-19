def run(ctx, args):
    import numpy as np
    breakpoints = sorted(args.get("breakpoints", []))
    heights = args.get("heights", [])
    
    # Add boundaries
    bp_full = [0.0] + sorted(breakpoints) + [2.0]
    h_vals = np.array(heights)
    
    # Discretize
    N = 800
    x = np.linspace(0, 2, N+1)
    h = np.zeros(N)
    
    for i in range(len(bp_full)-1):
        b0, b1 = bp_full[i], bp_full[i+1]
        if i < len(h_vals):
            # Fraction of intervals in this bin
            num_intervals = int((b1 - b0) * N / 2.0 + 0.5)
            start = int(b0 * N / 2.0)
            end = start + num_intervals
            for j in range(start, min(end, N)):
                h[j] = h_vals[i]
    
    # Enforce [0,1] and [0,2] bounds
    h = np.clip(h, 0.0, 1.0)
    
    # Normalize to ensure integral = 1
    integral = h.sum() * 2.0 / N
    if integral > 0:
        h = h / integral
    
    # Check constraints
    if np.min(h) < 0 or np.max(h) > 1:
        return {"error": "Height constraints violated", "h_norm": float(np.min(h)), "max_h": float(np.max(h))}
    
    if abs((h * 2.0 / N).sum() - 1.0) > 0.01:
        return {"error": "Integral constraint not met", "integral": float((h * 2.0 / N).sum())}
    
    return {"h": h.tolist(), "integral": float((h * 2.0 / N).sum()),
            "num_breaks": len(breakpoints)}
