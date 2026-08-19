def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    x = np.linspace(0, 2, N)
    
    def compute_c5(h):
        j_val = 1.0 - h
        h_padded = np.pad(h, (0, N))
        j_padded = np.pad(j_val, (0, N))
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        return float(np.max(correlation * dx))
    
    def normalize(h):
        integral = np.sum(h) * dx
        return h / integral
    
    candidates = []
    
    # Pattern 1: Piecewise-constant 3-block (low-high-low)
    np.random.seed(42)
    h = np.zeros(N)
    h[100:300] = 3.0
    h[300:700] = -0.5
    h[700:800] = 0.5
    h = normalize(np.clip(h, 0.001, 5.0))
    c5 = compute_c5(h)
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx),
                      "c5_bound": float(c5), "pattern": "piecewise3"})
    
    # Pattern 2: Two-block with offset
    np.random.seed(123)
    h = np.zeros(N)
    h[0:200] = 2.0
    h[200:600] = -1.0
    h[600:800] = 1.5
    h = normalize(np.clip(h, 0.001, 5.0))
    c5 = compute_c5(h)
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx),
                      "c5_bound": float(c5), "pattern": "twoblock"})
    
    # Pattern 3: Single-frequency sinusoidal
    np.random.seed(456)
    A = 2.0 + np.random.rand()
    B = np.random.uniform(-0.5, 0.5)
    h = 1.0 / (1.0 + np.exp(-(A * np.sin(np.pi * x) + B)))
    h = normalize(np.clip(h, 0.001, 1.0))
    c5 = compute_c5(h)
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx),
                      "c5_bound": float(c5), "pattern": "sin1freq"})
    
    # Pattern 4: Two-frequency sinusoidal
    np.random.seed(789)
    A = 1.5 + np.random.rand()
    B = np.random.uniform(-0.5, 0.5)
    C = np.random.uniform(-0.3, 0.3)
    h = 1.0 / (1.0 + np.exp(-(A * np.sin(2 * np.pi * x) + B * np.sin(4 * np.pi * x) + C)))
    h = normalize(np.clip(h, 0.001, 1.0))
    c5 = compute_c5(h)
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx),
                      "c5_bound": float(c5), "pattern": "sin2freq"})
    
    # Pattern 5: Quadratic bump
    np.random.seed(101)
    A = 3.0 + np.random.rand() * 2
    B = np.random.uniform(0.3, 0.7)
    h = 1.0 / (1.0 + np.exp(-A * (x - 1.0)**2 + B))
    h = normalize(np.clip(h, 0.001, 1.0))
    c5 = compute_c5(h)
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx),
                      "c5_bound": float(c5), "pattern": "quadbump"})
    
    return {"candidates": candidates, "num_candidates": len(candidates)}
