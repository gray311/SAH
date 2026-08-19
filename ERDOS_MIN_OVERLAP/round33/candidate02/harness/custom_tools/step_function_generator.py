def run(ctx, args):
    import numpy as np
    import json
    
    pattern = args.get("pattern", "bipartite")
    threshold = args.get("threshold", 0.5)
    num_peaks = args.get("num_peaks", 3)
    
    N = 800  # Use same num_intervals as seed
    domain = 2.0
    x = np.linspace(0, domain, N)
    
    if pattern == "bipartite":
        # h(x) = 1 for x < threshold, 0 otherwise
        h = np.zeros(N)
        h[x < threshold] = 1.0
        
    elif pattern == "multi_peak":
        # Create num_peaks narrow peaks with equal mass
        peak_width = 0.08
        peak_height = 1.0
        h = np.zeros(N)
        positions = np.linspace(0.2, 1.8, num_peaks)
        for pos in positions:
            h[np.abs(x - pos) < peak_width/2] = peak_height
        
    elif pattern == "golomb":
        # Golomb ruler-like: marks at [0, 0.4, 0.8, 1.2, 1.6]
        marks = np.array([0.0, 0.4, 0.8, 1.2, 1.6])
        peak_width = 0.06
        h = np.zeros(N)
        for mark in marks:
            h[np.abs(x - mark) < peak_width/2] = 1.0
    
    # Normalize to ensure integral = 1
    # integral(h) = sum(h) * dx = 1
    dx = domain / N
    current_integral = np.sum(h) * dx
    if current_integral > 0:
        h = h / current_integral
    
    # Ensure h in [0, 1]
    h = np.clip(h, 0, 1)
    
    # Pad to match seed program's expectations (pad with 0 at the end)
    h_padded = np.pad(h, (0, N))
    
    return {
        "pattern": pattern,
        "h_values": h.tolist(),
        "num_intervals": N,
        "integral_check": float(np.sum(h) * dx),
        "note": f"Generated {pattern} step function with integral={np.sum(h) * dx:.6f}"
    }
