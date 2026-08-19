def run(ctx, args):
    import numpy as np
    N = args.get("num_intervals", 100)
    heights = args.get("heights", None)
    custom_breakpoints = args.get("custom_breakpoints", None)
    
    dx = 2.0 / N
    
    # Generate breakpoints
    if custom_breakpoints is None:
        if heights is not None:
            # Use provided heights
            heights_arr = np.array(heights, dtype=np.float64)
            if len(heights_arr) != N:
                # Try to adjust to match N
                if len(heights_arr) > N:
                    heights_arr = heights_arr[:N]
                else:
                    # Repeat and truncate
                    repeats = (N + len(heights_arr) - 1) // len(heights_arr)
                    heights_arr = np.tile(heights_arr, repeats)[:N]
            h = np.zeros(N)
            for i, hi in enumerate(heights_arr):
                if 0 <= hi <= 1:
                    h = np.where(h % N == i, hi, h)
        else:
            # Default: start with 5-interval configuration
            N = 5
            # Pattern: [1, 0, 0, 0, 0] scaled to integrate to 1
            # With uniform intervals, h[i] * dx * N = 1, so h[i] = 1/N for all i
            # But we want concentration: try [1, 0, 0, 0, 0] style
            h = np.zeros(N)
            h[0] = 1.0
            # Scale to ensure integral = 1
            # integral = sum(h) * dx = 1 * 2/5 = 0.4, not 1
            # So we need h[0] = N/2 = 2.5, but that's > 1
            # Alternative: use [0.5, 0.5, 0, 0, 0] -> integral = 1 * 2/5 = 0.4
            # Need 2.5 total mass: [0.5, 0.5, 0.5, 0.5, 0]
            h = np.zeros(N)
            total_mass = N / 2.0
            h = np.ones(N) * total_mass / N
    
    # Ensure valid range
    h = np.clip(h, 0, 1)
    
    # Verify and adjust for integral = 1
    integral = np.sum(h) * dx
    if abs(integral - 1.0) > 0.01 and np.sum(h) > 0:
        scale = 1.0 / integral
        h = h * scale
        h = np.clip(h, 0, 1)
    
    return {
        "h": h.tolist(),
        "num_intervals": N,
        "integral": float(np.sum(h) * dx),
        "min_h": float(np.min(h)),
        "max_h": float(np.max(h)),
        "valid": 0.0 <= np.min(h) and np.max(h) <= 1.0 and abs(np.sum(h) * dx - 1.0) < 0.01
    }
