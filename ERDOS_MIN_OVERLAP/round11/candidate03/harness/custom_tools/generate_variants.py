def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    rng = np.random.default_rng(123)
    constructions = {}
    
    # 1. asymmetric_bimodal: Two peaks at different heights/locations
    x = np.linspace(0, domain, N)
    h1 = np.exp(-((x - 0.2) / 0.15)**2 * 15)
    h2 = np.exp(-((x - 0.8) / 0.12)**2 * 12)
    latent = (h1 + h2) / (np.max(h1+h2) + 1e-10)
    constructions['asymmetric_bimodal'] = latent
    
    # 2. symmetric_bimodal: Two equal peaks (for comparison)
    latent = np.exp(-((x - 0.25) / 0.15)**2 * 15) + np.exp(-((x - 0.75) / 0.15)**2 * 15)
    latent = (latent - np.min(latent)) / (np.max(latent) - np.min(latent) + 1e-10)
    constructions['symmetric_bimodal'] = latent
    
    # 3. tri_modal: Three peaks with varying widths
    latent = np.zeros(N)
    latent += np.exp(-((x - 0.15) / 0.12)**2 * 12)
    latent += np.exp(-((x - 0.5) / 0.15)**2 * 10)
    latent += np.exp(-((x - 0.95) / 0.11)**2 * 13)
    latent = (latent - np.min(latent)) / (np.max(latent) - np.min(latent) + 1e-10)
    constructions['tri_modal'] = latent
    
    # 4. periodic_3: Three-level alternating pattern
    phases = np.array([0.0, 0.5, 1.0])
    levels = np.array([5, -5, 5])
    latent = np.zeros(N)
    for p, l in zip(phases, levels):
        in_range = (x >= p) & (x < p + 0.5)
        latent += l * in_range
    latent += rng.normal(size=N) * 0.2
    constructions['periodic_3'] = latent
    
    # 5. multi_peak_4: Four narrow peaks with optimal-ish spacing
    marks = np.array([0.1, 0.4, 0.7, 1.0])
    widths = np.array([0.08, 0.09, 0.08, 0.09])
    latent = np.zeros(N)
    for m, w in zip(marks, widths):
        latent += np.exp(-((x - m) / w)**2 * 18)
    latent = (latent - np.min(latent)) / (np.max(latent) - np.min(latent) + 1e-10)
    constructions['multi_peak_4'] = latent
    
    return {"constructions": constructions, "keys_used": list(constructions.keys())}
