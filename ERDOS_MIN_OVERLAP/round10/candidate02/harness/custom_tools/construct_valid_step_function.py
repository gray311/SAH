def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    rng = np.random.default_rng(123)
    
    def normalize_to_integral_1(l, x):
        """Adjust latent to get integral(h) = 1 using iterative threshold shift."""
        h = 1 / (1 + np.exp(-l))
        integral = np.sum(h) * dx
        
        # Iteratively adjust to get integral = 1
        for _ in range(100):
            if abs(integral - 1.0) < 1e-6:
                break
            # Compute log-derivative of integral w.r.t. latent threshold
            shift = (integral - 1.0) / (np.sum(np.exp(-l))) * 2.0
            l = l - shift
            h = 1 / (1 + np.exp(-l))
            integral = np.sum(h) * dx
        return l
    
    candidates = {}
    
    # Bimodal: two narrow peaks
    x = np.linspace(0, domain, N)
    bw1, bw2 = 0.15, 0.15
    for pos1, pos2 in [(0.25, 0.75), (0.2, 0.8), (0.1, 0.9), (0.3, 0.7)]:
        l = -((x-pos1)/bw1)**2 * 30 - ((x-pos2)/bw2)**2 * 30
        l = l - np.mean(l)
        l_norm = normalize_to_integral_1(l, x)
        candidates[f'bimodal_{pos1}_{pos2}'] = l_norm
    
    # Triangular 3-level patterns
    phases = [0.0, 0.33, 0.66]
    for levels in [([-4, -1, 4]), ([-3, 0, 3]), ([-2, 1, 5])]:
        l = np.zeros(N)
        for p, lev in zip(phases, levels):
            in_range = (x >= p) & (x < p + 0.33)
            l = l + lev * in_range
        l_norm = normalize_to_integral_1(l, x)
        candidates[f'triangular_{levels}'] = l_norm
    
    # Periodic: on/off patterns with varying duty cycle
    for p in [0.3, 0.25, 0.4, 0.35]:
        l = np.where(x < p, 5.0, -5.0) + rng.normal(size=N) * 0.3
        l_norm = normalize_to_integral_1(l, x)
        candidates[f'periodic_{p}'] = l_norm
    
    # Golomb ruler inspired: 5 peaks at optimal spacing
    marks = np.array([0.0, 0.5, 1.25, 1.625, 2.0])
    widths = np.array([0.12, 0.10, 0.09, 0.09, 0.11])
    l = np.zeros(N)
    for m, w in zip(marks, widths):
        l = l + 8.0 * np.exp(-((x-m)/w)**2 * 25)
    l_norm = normalize_to_integral_1(l, x)
    candidates['golomb_5'] = l_norm
    
    # Asymmetric single peak variants
    for pos in [0.1, 0.2, 0.4, 0.6]:
        l = -((x-pos)/0.2)**2 * 40
        l = l - np.mean(l)
        l_norm = normalize_to_integral_1(l, x)
        candidates[f'asymmetric_{pos}'] = l_norm
    
    return {"candidates": candidates, "num_candidates": len(candidates)}
