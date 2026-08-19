def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    rng = np.random.default_rng(123)
    patterns = {}
    x = np.linspace(0, domain, N)
    
    # 1. Bimodal hard: Two sharp peaks thresholded
    a1, a2 = 0.25, 0.75
    bw1, bw2 = 0.12, 0.12
    latent = np.exp(-((x-a1)/bw1)**2 * 25) + np.exp(-((x-a2)/bw2)**2 * 25)
    h = np.clip(np.array([1.0 if v > 0.3 else 0.0 for v in latent]), 0, 1)
    h_norm = h / np.sum(h) * N
    patterns["bimodal_hard"] = h_norm
    
    # 2. Golomb-5 hard: 5 peaks at optimal spacing
    marks = np.array([0.0, 0.5, 1.25, 1.75, 2.0])
    bws = np.array([0.08, 0.08, 0.09, 0.09, 0.1])
    latent = np.zeros(N)
    for m, bw in zip(marks, bws):
        latent += np.exp(-((x-m)/bw)**2 * 30)
    h = np.clip(np.array([1.0 if v > 0.2 else 0.0 for v in latent]), 0, 1)
    h_norm = h / np.sum(h) * N
    patterns["golomb_5_hard"] = h_norm
    
    # 3. Triangular hard: 3-level linear pattern
    levels = [0.0, 0.5, 1.0]
    starts = [0.0, 0.666, 1.333]
    h_tri = np.zeros(N)
    for s, l in zip(starts, levels):
        h_tri = np.where(x >= s, h_tri + l, h_tri)
    h_tri = np.clip(h_tri, 0, 1)
    h_tri = h_tri / np.sum(h_tri) * N
    patterns["triangular_hard"] = h_tri
    
    # 4. Periodic hard: alternating with duty cycle
    duty = 0.4
    h_per = np.where(x < 0.5 * duty, 1.0, 0.0)
    h_per_norm = h_per / np.sum(h_per) * N
    patterns["periodic_hard"] = h_per_norm
    
    # 5. Random shifted peaks
    np.random.seed(456)
    np.random.seed(789)
    num_peaks = 5
    peak_positions = np.sort(np.random.uniform(0.1, 1.9, num_peaks))
    bw = 0.1
    latent = np.zeros(N)
    for p in peak_positions:
        latent += np.exp(-((x-p)/bw)**2 * 20)
    h_rand = np.clip(np.array([1.0 if v > 0.25 else 0.0 for v in latent]), 0, 1)
    h_rand = h_rand / np.sum(h_rand) * N
    patterns["random_shifted"] = h_rand
    
    return {"patterns": patterns, "pattern_keys": list(patterns.keys())}