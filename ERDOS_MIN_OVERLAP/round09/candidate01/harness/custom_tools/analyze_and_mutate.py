def run(ctx, args):
    import numpy as np
    import math
    
    N = 800
    domain = 2.0
    dx = domain / N
    x = np.linspace(0, domain, N)
    
    mutants = []
    
    splits = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    for split in splits:
        h_val = np.zeros(N)
        if split < 1.0:
            p1 = split * 0.8
            p2 = (2.0 - split) * 0.8 + split
        else:
            p1 = split - 0.2
            p2 = split + 0.2
        
        w1, w2 = 0.12, 0.12
        h_val = np.exp(-((x - p1) / w1) ** 2 * 30) + np.exp(-((x - p2) / w2) ** 2 * 30)
        
        integral = np.sum(h_val) * dx
        if integral > 0:
            scale = 1.0 / integral
            h_val = h_val * scale
        
        latent = np.log(h_val / (1.0 - h_val + 1e-10))
        latent[latent < -20] = -20
        mutants.append({"type": "bimodal_split", "split": float(split), "latent": latent})
    
    base_positions = [0.25, 0.75]
    for delta in [-0.05, 0, 0.05]:
        shifted_positions = [p + delta for p in base_positions]
        latent = np.zeros(N)
        for pos in shifted_positions:
            w = 0.12
            latent += np.exp(-((x - pos) / w) ** 2 * 30)
        
        integral = np.sum(np.maximum(0, latent)) * dx
        if integral > 0:
            scale = 1.0 / integral
            latent = np.log(np.maximum(1e-10, latent) / (1.0 - np.maximum(1e-10, latent) + 1e-10))
            latent[latent < -20] = -20
        else:
            latent = np.zeros(N)
        mutants.append({"type": "shifted_peaks", "delta": float(delta), "latent": latent})
    
    asymmetric_configs = [
        ([0.25, 0.75], [0.12, 0.18]),
        ([0.25, 0.75], [0.18, 0.12]),
        ([0.2, 0.7], [0.1, 0.15]),
        ([0.3, 0.7], [0.15, 0.10]),
    ]
    
    for positions, widths in asymmetric_configs:
        latent = np.zeros(N)
        for pos, w in zip(positions, widths):
            latent += np.exp(-((x - pos) / w) ** 2 * 30)
        
        integral = np.sum(np.maximum(0, latent)) * dx
        if integral > 0:
            scale = 1.0 / integral
            latent = np.log(np.maximum(1e-10, latent) / (1.0 - np.maximum(1e-10, latent) + 1e-10))
            latent[latent < -20] = -20
        else:
            latent = np.zeros(N)
        mutants.append({"type": "asymmetric", "latent": latent})
    
    for base_x in [0.1, 0.15, 0.2, 0.25]:
        p1 = base_x
        p2 = base_x + 1.0
        w = 0.12
        latent = np.exp(-((x - p1) / w) ** 2 * 30) + np.exp(-((x - p2) / w) ** 2 * 30)
        integral = np.sum(np.maximum(0, latent)) * dx
        if integral > 0:
            scale = 1.0 / integral
            latent = np.log(np.maximum(1e-10, latent) / (1.0 - np.maximum(1e-10, latent) + 1e-10))
            latent[latent < -20] = -20
        else:
            latent = np.zeros(N)
        mutants.append({"type": "phase_shift", "base_x": float(base_x), "latent": latent})
    
    return {"mutants": mutants, "count": len(mutants)}
