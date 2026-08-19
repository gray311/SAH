def run(ctx, args):
    import numpy as np
    structure = args.get("structure", "bimodal")
    params = args.get("params", {})
    
    N = 800
    domain = 2.0
    dx = domain / N
    h = np.zeros(N)
    
    if structure == "bipartite":
        # Single threshold: h=1 for x < threshold * 2
        threshold = params.get("threshold", 0.5)
        cutoff = threshold * 2
        mask = np.arange(N) * dx < cutoff
        h[mask] = 1.0
    
    elif structure == "bimodal":
        # Two peaks
        positions = params.get("peak_positions", [0.3, 1.7])
        widths = params.get("peak_widths", [0.2, 0.2])
        for pos, width in zip(positions, widths):
            left = max(0, pos - width/2)
            right = min(2, pos + width/2)
            mask = (np.arange(N) * dx >= left) & (np.arange(N) * dx < right)
            h[mask] = 1.0
    
    elif structure == "trimodal":
        # Three peaks
        positions = params.get("peak_positions", [0.33, 1.0, 1.67])
        widths = params.get("peak_widths", [0.15, 0.3, 0.15])
        for pos, width in zip(positions, widths):
            left = max(0, pos - width/2)
            right = min(2, pos + width/2)
            mask = (np.arange(N) * dx >= left) & (np.arange(N) * dx < right)
            h[mask] = 1.0
    
    elif structure == "sparse":
        # Very sparse: non-zero on small total width
        total_width = params.get("total_width", 0.5)
        positions = params.get("peak_positions", [0.5, 1.0, 1.5])
        num_peaks = len(positions)
        width_per_peak = total_width / num_peaks
        for pos, width in zip(positions, [width_per_peak]*num_peaks):
            left = max(0, pos - width/2)
            right = min(2, pos + width/2)
            mask = (np.arange(N) * dx >= left) & (np.arange(N) * dx < right)
            h[mask] = 1.0
    
    # Verify integral constraint
    integral = np.sum(h) * dx
    return {"h": h.tolist(), "integral": float(integral), "structure": structure}
