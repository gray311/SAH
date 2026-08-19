def run(ctx, args):
    import random
    import numpy as np
    
    pattern_type = args.get("pattern_type", "bipolar")
    seed = args.get("seed", 42)
    random.seed(seed)
    
    N = 800  # Number of intervals
    domain = 2.0
    dx = domain / N
    
    h = np.zeros(N)
    
    if pattern_type == "bipartite":
        # Single threshold at t in (0,2), h=1 for x<t, h=0 for x>=t
        t = random.uniform(0.3, 1.7)
        h[:int(t*N/dx)] = 1.0
        # Normalize to integral = 1
        integral = h.sum() * dx
        if integral > 0:
            h = h / integral
        
    elif pattern_type == "bipolar":
        # Two peaks at p1, p2
        p1 = random.uniform(0.2, 0.8)
        p2 = random.uniform(1.2, 1.8)
        width1 = random.uniform(0.15, 0.25)
        width2 = random.uniform(0.15, 0.25)
        height1 = random.uniform(0.8, 1.0)
        height2 = random.uniform(0.8, 1.0)
        
        # Create peaks with Gaussian-like shapes, then threshold to [0,1]
        x = np.linspace(0, 2, N)
        peak1 = np.exp(-((x - p1) ** 2) / (2 * width1**2))
        peak2 = np.exp(-((x - p2) ** 2) / (2 * width2**2))
        h = (peak1 * height1 + peak2 * height2)
        h = np.clip(h, 0, 1)
        
    elif pattern_type == "tripolar":
        # Three peaks, often symmetric around x=1
        centers = [0.4, 1.0, 1.6]
        widths = [0.12, 0.12, 0.12]
        heights = [0.8, 1.0, 0.8]
        
        x = np.linspace(0, 2, N)
        h = np.zeros(N)
        for c, w, ht in zip(centers, widths, heights):
            peak = np.exp(-((x - c) ** 2) / (2 * w**2))
            h += peak * ht
        h = np.clip(h, 0, 1)
        
    elif pattern_type == "four-modal":
        # Four peaks with spacing to minimize overlap
        centers = [0.25, 0.75, 1.25, 1.75]
        widths = [0.1, 0.1, 0.1, 0.1]
        heights = [0.7, 0.9, 0.9, 0.7]
        
        x = np.linspace(0, 2, N)
        h = np.zeros(N)
        for c, w, ht in zip(centers, widths, heights):
            peak = np.exp(-((x - c) ** 2) / (2 * w**2))
            h += peak * ht
        h = np.clip(h, 0, 1)
        
    elif pattern_type == "golomb":
        # Golomb ruler inspired: peaks at 0.0, 0.4, 0.8, 1.2, 1.6
        centers = [0.0, 0.4, 0.8, 1.2, 1.6]
        widths = [0.12, 0.12, 0.12, 0.12, 0.12]
        heights = [0.8, 0.9, 0.85, 0.9, 0.8]
        
        x = np.linspace(0, 2, N)
        h = np.zeros(N)
        for c, w, ht in zip(centers, widths, heights):
            peak = np.exp(-((x - c) ** 2) / (2 * w**2))
            h += peak * ht
        h = np.clip(h, 0, 1)
    
    # Ensure h is in [0,1] and integral is approximately 1
    h = np.clip(h, 0, 1)
    integral = h.sum() * dx
    
    if integral > 0 and integral < 1e-6:
        h = h / integral
    
    # Return the h array as a string representation
    h_str = ",".join([f"{x:.6f}" for x in h])
    return {
        "pattern": pattern_type,
        "integral": float(integral),
        "h_array": h_str
    }
