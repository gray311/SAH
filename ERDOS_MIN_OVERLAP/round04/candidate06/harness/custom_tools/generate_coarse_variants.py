def run(ctx, args):
    import numpy as np
    rng = np.random.default_rng(123)
    N_coarse = 40
    domain = 2.0
    x_arr = np.linspace(0, domain, N_coarse)
    
    variants = {}
    
    # Strategy 1: Single peak bimodal
    latent = np.zeros(N_coarse)
    peak_pos = rng.uniform(0.2, 0.8)
    peak_width = rng.uniform(0.05, 0.15)
    for i in range(N_coarse):
        if abs(x_arr[i] - peak_pos) < peak_width:
            latent[i] = 8.0
    latent = latent + rng.normal(size=N_coarse) * 0.5
    variants["bimodal_coarse"] = (latent, {"optimizer": "sgd_momentum", "lr_schedule": [0.05, 0.01, 0.001]})
    
    # Strategy 2: Three-level plateau
    latent = np.zeros(N_coarse)
    boundaries = [rng.uniform(0.1, 0.3), rng.uniform(0.3, 0.6), rng.uniform(0.6, 0.85), rng.uniform(0.85, 0.95)]
    for i in range(N_coarse):
        for idx in range(len(boundaries)-1):
            if boundaries[idx] <= x_arr[i] < boundaries[idx+1]:
                latent[i] = 5.0 + rng.uniform(-0.5, 0.5)
                break
    latent = latent + rng.normal(size=N_coarse) * 0.3
    variants["three_plateau"] = (latent, {"optimizer": "lbgfs", "lr_schedule": [0.01]})
    
    # Strategy 3: Periodic blocks
    latent = np.zeros(N_coarse)
    for start, end in [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0), (1.0, 1.5), (1.5, 2.0)]:
        if start < end:
            for i in range(N_coarse):
                if start <= x_arr[i] < end:
                    latent[i] = 6.0
                elif start + 0.5 <= x_arr[i] < end + 0.5:
                    latent[i] = -2.0
    latent = latent + rng.normal(size=N_coarse) * 0.2
    variants["periodic_blocks"] = (latent, {"optimizer": "adam_coarse", "lr_schedule": [0.03, 0.005]})
    
    # Strategy 4: Golomb-inspired (5 peaks)
    marks = [0.2, 0.35, 0.6, 0.7, 1.1]
    latent = np.zeros(N_coarse)
    for m in marks:
        w = 0.08
        for i in range(N_coarse):
            latent[i] += 7.0 * np.exp(-((x_arr[i] - m)/w)**2 * 10)
    latent = latent + rng.normal(size=N_coarse) * 0.3
    variants["golomb_coarse"] = (latent, {"optimizer": "lbgfs", "lr_schedule": [0.01]})
    
    # Strategy 5: Random threshold
    thresholds = np.sort(np.random.uniform(0.1, 0.9, size=8))
    current_level = 5.0
    latent = np.zeros(N_coarse)
    for i, t in enumerate(thresholds):
        for j in range(N_coarse):
            if x_arr[j] >= t:
                if i == 0 or (x_arr[j] < t + np.random.uniform(0.1, 0.25)):
                    latent[j] = current_level
                else:
                    latent[j] = current_level - rng.uniform(1.0, 3.0)
            else:
                break
    latent = latent + rng.normal(size=N_coarse) * 0.25
    variants["random_threshold"] = (latent, {"optimizer": "sgd_momentum", "lr_schedule": [0.04, 0.008]})
    
    return {"variants": variants, "N_coarse": N_coarse, "domain": domain, "dx": domain / N_coarse}
