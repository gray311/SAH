def run(ctx, args):
    import numpy as np
    N_intervals = 800
    domain = 2.0
    dx = domain / N_intervals
    
    def compute_c5(h):
        h_padded = np.pad(h, (0, N_intervals))
        j_padded = np.pad(1.0 - h, (0, N_intervals))
        corr = np.fft.ifft(np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))).real
        return float(np.max(corr) * dx)
    
    def scale_to_integral_one(h):
        integral = np.sum(h) * dx
        if integral < 1e-6:
            return h
        return h / integral
    
    np.random.seed(42)
    candidates = []
    x = np.linspace(0, 2, N_intervals)
    
    # Grid 1: Binary step functions, N=4 to 12
    for num_steps in [4, 6, 8, 10, 12]:
        midpoints = np.linspace(0, 2, num_steps + 1)[1:-1]
        levels = np.random.choice([0, 0.5, 1.0], size=num_steps)
        h = np.zeros(N_intervals)
        for i, mid in enumerate(midpoints):
            mask = x < mid
            h[mask] = levels[i]
        h = scale_to_integral_one(h)
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "c5_bound": c5, "structure": f"binary_N{num_steps}", "c5_raw": c5})
    
    # Grid 2: Golden-ratio spacing
    np.random.seed(43)
    golden = 1.618034
    phi_points = [0.0]
    for i in range(8):
        phi_points.append(2.0 * (golden**i) % 2.0)
    phi_points.append(2.0)
    phi_points = sorted(set([round(p, 4) for p in phi_points]))
    h = np.zeros(N_intervals)
    for i in range(len(phi_points)-1):
        h[(x >= phi_points[i]) & (x < phi_points[i+1])] = 0.5 + np.random.rand() * 0.5
    h = scale_to_integral_one(h)
    c5 = compute_c5(h)
    candidates.append({"h": h.tolist(), "c5_bound": c5, "structure": "golden_N8", "c5_raw": c5})
    
    # Grid 3: Fibonacci-like spacing
    np.random.seed(44)
    fib_pts = [0.0, 0.382, 0.618, 1.0, 1.382, 1.618, 2.0]
    h = np.zeros(N_intervals)
    for i in range(len(fib_pts)-1):
        h[(x >= fib_pts[i]) & (x < fib_pts[i+1])] = np.random.choice([0, 0.5, 1.0])
    h = scale_to_integral_one(h)
    c5 = compute_c5(h)
    candidates.append({"h": h.tolist(), "c5_bound": c5, "structure": "fibonacci_N6", "c5_raw": c5})
    
    # Grid 4: Uniform with perturbation
    np.random.seed(45)
    level_x = np.linspace(0, 2, 20)
    levels = np.random.choice([0, 0.25, 0.5, 0.75, 1.0], size=20)
    h = np.zeros(N_intervals)
    for i in range(19):
        left, right = level_x[i], level_x[i+1]
        fraction = (right - left) / 2.0
        h[(x >= left - fraction) & (x < left + fraction)] = levels[i]
    h = scale_to_integral_one(h)
    c5 = compute_c5(h)
    candidates.append({"h": h.tolist(), "c5_bound": c5, "structure": "uniform_20_bands", "c5_raw": c5})
    
    return {"candidates": candidates, "num_candidates": len(candidates)}
