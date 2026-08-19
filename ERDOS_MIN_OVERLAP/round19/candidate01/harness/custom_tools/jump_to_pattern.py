def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    x = np.linspace(0, 2, N)
    seed = args.get("seed", 0)
    np.random.seed(seed)
    
    def normalize_to_integral_1(h):
        integral = np.sum(h) * dx
        if integral == 0:
            return h
        return h / integral
    
    h_raw = np.zeros(N)
    c5_val = np.inf
    
    structure = args.get("structure", "two-level")
    
    if structure == "two-level":
        a = 0.3 + np.random.rand() * 0.4  # left edge
        b = 1.7 + np.random.rand() * 0.4  # right edge
        h_raw = np.zeros(N)
        h_raw[x > a] = 0.0
        h_raw[x <= a] = 2.0  # will normalize to integral=1
        
        # Normalize
        h_raw = normalize_to_integral_1(h_raw)
        
    elif structure == "three-level":
        a = 0.3 + np.random.rand() * 0.4
        b = 0.7 + np.random.rand() * 0.4
        h_raw = np.zeros(N)
        h_raw[x > b] = 0.0
        h_raw[(a, b)] = 2.0  # middle region higher
        h_raw[x <= a] = 1.0  # left region lower
        
        h_raw = normalize_to_integral_1(h_raw)
        
    elif structure == "golomb":
        marks = np.array([0.2, 0.6, 1.0, 1.4, 1.8])
        h_raw = np.zeros(N)
        for m in marks:
            h_raw += 3.0 * np.exp(-((x - m) / 0.15)**2)
        h_raw = normalize_to_integral_1(h_raw)
        
    elif structure == "sinusoidal":
        x_local = x * np.pi
        h_raw = 0.5 + 0.3 * np.sin(x_local) + 0.2 * np.sin(2 * x_local)
        h_raw = np.clip(h_raw, 0.01, 5.0)
        h_raw = normalize_to_integral_1(h_raw)
    
    # Compute c5 bound
    h_padded = np.pad(h_raw, (0, N))
    j_raw = 1.0 - h_raw
    j_padded = np.pad(j_raw, (0, N))
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    c5_bound = float(np.max(correlation * dx))
    
    return {
        "h": h_raw.tolist(),
        "c5_bound": c5_bound,
        "integral": float(np.sum(h_raw) * dx),
        "structure": structure
    }
