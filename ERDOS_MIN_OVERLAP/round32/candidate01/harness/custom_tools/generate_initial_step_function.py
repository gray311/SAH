def run(ctx, args):
    import numpy as np
    import random
    
    num_intervals = 800
    domain = 2.0
    dx = domain / num_intervals
    
    candidates = []
    
    # Type 1: Bipartite
    threshold = np.random.uniform(0.3, 0.7)
    h = np.where(np.linspace(0, 2, num_intervals) < threshold, 1.0, 0.0)
    integral = np.sum(h) * dx
    h = h / (integral / num_intervals)
    h = np.clip(h, 0, 1)
    candidates.append(h)
    
    # Type 2: Two peaks
    peak1 = np.random.uniform(0.2, 0.5)
    peak2 = np.random.uniform(1.5, 1.8)
    width = np.random.uniform(0.1, 0.2)
    h = np.zeros(num_intervals)
    h[np.abs(np.linspace(0, 2, num_intervals) - peak1) < width] = 1.0
    h[np.abs(np.linspace(0, 2, num_intervals) - peak2) < width] = 1.0
    integral = np.sum(h) * dx
    h = h / (integral / num_intervals)
    h = np.clip(h, 0, 1)
    candidates.append(h)
    
    # Type 3: Three peaks
    centers = [np.random.uniform(0.2, 0.4), 
              np.random.uniform(0.8, 1.0),
              np.random.uniform(1.4, 1.6)]
    width = np.random.uniform(0.1, 0.15)
    h = np.zeros(num_intervals)
    for c in centers:
        h[np.abs(np.linspace(0, 2, num_intervals) - c) < width] = 1.0
    integral = np.sum(h) * dx
    h = h / (integral / num_intervals)
    h = np.clip(h, 0, 1)
    candidates.append(h)
    
    chosen = random.choice(candidates)
    return {
        "h": chosen.tolist(),
        "num_intervals": num_intervals,
        "integral_check": float(np.sum(chosen) * dx),
        "type": random.choice(["bipartite", "two_peaks", "three_peaks"])
    }
