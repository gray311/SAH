def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    rng = np.random.default_rng(123)
    
    constructions = {}
    x = np.linspace(0, domain, N)
    
    # Binary 2-peak
    h = np.zeros(N)
    h[(x >= 0.4) & (x <= 0.6)] = 1.0
    h[(x >= 1.0) & (x <= 1.4)] = 1.0
    s = np.sum(h)
    h = h * N / s if s > 0 else h
    constructions['binary_2peak'] = h
    
    # Binary 3-peak
    h = np.zeros(N)
    h[(x >= 0.25) & (x <= 0.45)] = 1.0
    h[(x >= 0.7) & (x <= 0.9)] = 1.0
    h[(x >= 1.3) & (x <= 1.5)] = 1.0
    s = np.sum(h)
    h = h * N / s if s > 0 else h
    constructions['binary_3peak'] = h
    
    # Periodic sin
    h = np.abs(np.sin(np.pi * x / 1.0)) ** 1.5
    s = np.sum(h)
    h = h * N / s if s > 0 else h
    constructions['periodic_sin'] = h
    
    # Periodic cos
    h = np.abs(np.cos(np.pi * (x - 1.0))) ** 1.5
    s = np.sum(h)
    h = h * N / s if s > 0 else h
    constructions['periodic_cos'] = h
    
    # Golomb 3 marks
    marks = np.array([0.333, 1.0, 1.666])
    bw = 0.08
    h = np.zeros(N)
    for m in marks:
        h += np.exp(-((x - m) / bw) ** 2 * 30)
    s = np.sum(h)
    h = h * N / s if s > 0 else h
    constructions['golomb_3'] = h
    
    # Golomb 5 marks
    marks = np.array([0.2, 0.5, 0.8, 1.3, 1.6])
    bw = 0.06
    h = np.zeros(N)
    for m in marks:
        h += np.exp(-((x - m) / bw) ** 2 * 30)
    s = np.sum(h)
    h = h * N / s if s > 0 else h
    constructions['golomb_5'] = h
    
    # Asymmetric left
    h = np.zeros(N)
    h[(x <= 0.33)] = 3.0
    h[(x > 0.33) & (x <= 1.33)] = 0.75
    h[(x > 1.33)] = 0.0
    s = np.sum(h)
    h = h * N / s if s > 0 else h
    constructions['asymmetric_left'] = h
    
    # Asymmetric right
    h = np.zeros(N)
    h[(x <= 0.66)] = 0.5
    h[(x > 0.66) & (x <= 1.66)] = 1.5
    h[(x > 1.66)] = 2.0
    s = np.sum(h)
    h = h * N / s if s > 0 else h
    constructions['asymmetric_right'] = h
    
    # Gaussian 2
    mu1, mu2 = 0.5, 1.5
    sigma = 0.15
    h = np.exp(-((x - mu1) / sigma) ** 2 * 10) + np.exp(-((x - mu2) / sigma) ** 2 * 10)
    s = np.sum(h)
    h = h * N / s if s > 0 else h
    constructions['gaussian_2'] = h
    
    # Gaussian 3
    mu = np.array([0.3, 0.8, 1.5])
    sigma = 0.12
    h = np.zeros(N)
    for m in mu:
        h += np.exp(-((x - m) / sigma) ** 2 * 15)
    s = np.sum(h)
    h = h * N / s if s > 0 else h
    constructions['gaussian_3'] = h
    
    # Triangular
    h = np.zeros(N)
    peaks = np.array([0.5, 1.0, 1.5])
    widths = np.array([0.4, 0.3, 0.3])
    for p, w in zip(peaks, widths):
        d = np.abs(x - p)
        h = h + np.maximum(0, w * (1 - d / (w/2)))
    s = np.sum(h)
    h = h * N / s if s > 0 else h
    constructions['triangular'] = h
    
    # Exponential decay pair
    h = np.exp(-10 * np.abs(x - 0.5)) + np.exp(-10 * np.abs(x - 1.5))
    s = np.sum(h)
    h = h * N / s if s > 0 else h
    constructions['exp_decay'] = h
    
    return {"constructions": constructions}
