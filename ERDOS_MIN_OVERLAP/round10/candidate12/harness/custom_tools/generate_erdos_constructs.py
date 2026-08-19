def run(ctx, args):
    import numpy as np
    N = 400
    domain = 2.0
    dx = domain / N
    rng = np.random.default_rng(123)
    constructions = {}
    
    # Construction 1: Tight bimodal with peaks at 0.25 and 0.75
    x = np.linspace(0, domain, N)
    latent1 = np.zeros(N)
    latent1[x < 0.4] = 5.0
    latent1[(x >= 0.4) & (x < 0.6)] = -3.0
    latent1[(x >= 0.6) & (x < 0.8)] = 5.0
    latent1[x >= 0.8] = -3.0
    latent1 = latent1 + rng.normal(size=N) * 0.3
    constructions['bimodal_tight'] = latent1
    
    # Construction 2: Three-level pattern
    x = np.linspace(0, domain, N)
    latent2 = np.zeros(N)
    latent2[x < 1/3] = -2.0
    latent2[(x >= 1/3) & (x < 2/3)] = 3.0
    latent2[x >= 2/3] = -2.0
    latent2 = latent2 + rng.normal(size=N) * 0.2
    constructions['triple_pattern'] = latent2
    
    # Construction 3: Golomb ruler-inspired (marks at 0, 1/4, 2/5, 9/10, 1)
    x = np.linspace(0, domain, N)
    marks = np.array([0.0, 0.25, 0.4, 0.9, 1.0])
    latent3 = np.zeros(N)
    for m in marks:
        latent3 = latent3 + 4.0 * np.exp(-((x - m) / 0.08) ** 2 * 10)
    latent3 = latent3 - np.mean(latent3)
    latent3 = latent3 + rng.normal(size=N) * 0.2
    constructions['golomb_5'] = latent3
    
    # Construction 4: Alternating blocks
    x = np.linspace(0, domain, N)
    latent4 = np.zeros(N)
    for i in range(4):
        start = i * 0.5 / 2
        end = (i + 1) * 0.5 / 2
        if i % 2 == 0:
            latent4[(x >= start) & (x < end)] = 3.0
        else:
            latent4[(x >= start) & (x < end)] = -3.0
    latent4 = latent4 + rng.normal(size=N) * 0.3
    constructions['alternating_4'] = latent4
    
    # Construction 5: Asymmetric bimodal
    x = np.linspace(0, domain, N)
    latent5 = np.zeros(N)
    latent5[x < 0.3] = -3.0
    latent5[(x >= 0.3) & (x < 0.7)] = 4.0
    latent5[x >= 0.7] = -3.0
    latent5 = latent5 + rng.normal(size=N) * 0.3
    constructions['asymmetric_bimodal'] = latent5
    
    return {"constructions": constructions, 
            "keys": list(constructions.keys()),
            "note": "Each construction uses a different structural strategy to escape local minima"}
