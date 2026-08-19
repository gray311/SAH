def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    constructions = {}
    
    # 1. Golomb ruler for 5 marks: [0, 1, 4, 9, 11] scaled
    golomb_pos = np.array([0.0, 0.5, 1.6, 3.75, 4.4]) * 0.444
    golomb_pos = golomb_pos / golomb_pos.max() * 2.0
    h = np.zeros(N)
    for pos in golomb_pos:
        idx = int(pos * N)
        width = 20
        start = max(0, idx - width)
        end = min(N, idx + width)
        count = end - start
        if count > 0:
            h[start:end] = np.linspace(1, 0, count)
    h = h / (np.sum(h) * domain + 1e-10)
    constructions['golomb_5'] = h
    
    # 2. Bipartite: high on [0,a] U [2-a,2], low in middle
    a = 0.5
    h = np.ones(N)
    h[int(N*a):int(N*(2-a))] = 0.2
    h = h / (np.sum(h) * domain + 1e-10)
    constructions['bipartite_a05'] = h
    
    # 3. Tri-modal: three peaks
    h = np.zeros(N)
    peaks = [150, 400, 650]
    for p in peaks:
        w = 80
        start = max(0, p - w)
        end = min(N, p + w)
        count = end - start
        if count > 0:
            h[start:end] = np.where(np.arange(count) > w, 0.0, 1.5)
    h = h / (np.sum(h) * domain + 1e-10)
    constructions['tri_modal'] = h
    
    # 4. Asymmetric triangular
    h = np.zeros(N)
    h[:int(N*0.4)] = 2.0
    h[int(N*0.4):int(N*1.2)] = 0.8
    h[int(N*1.2):] = -0.5
    h = np.clip(h, 0, 5)
    h = h / (np.sum(h) * domain + 1e-10)
    constructions['asym_tri'] = h
    
    # 5. Sawtooth
    h = np.zeros(N)
    count = N
    if count > 0:
        h[:] = np.linspace(0, 3, count)
    h = h / (np.sum(h) * domain + 1e-10)
    constructions['sawtooth'] = h
    
    # 6. Exponential decay from left
    x = np.linspace(0, 2, N)
    h = np.exp(-2 * x)
    h = h / (np.sum(h) * domain + 1e-10)
    constructions['exp_decay'] = h
    
    # 7. Ramp function
    h = np.linspace(0.3, 1.7, N)
    h = h / (np.sum(h) * domain + 1e-10)
    constructions['ramp'] = h
    
    # 8. Step at midpoint
    h = np.zeros(N)
    h[int(N*0.5):] = 1.5
    h = h / (np.sum(h) * domain + 1e-10)
    constructions['step_mid'] = h
    
    # 9. Sinusoidal-biased
    x = np.linspace(0, 2, N)
    h = 0.5 + 0.5 * np.sin(2 * np.pi * x / 2)
    h = np.clip(h, 0.1, 0.99)
    h = h / (np.sum(h) * domain + 1e-10)
    constructions['sin_bias'] = h
    
    # 10. Piecewise-constant with 4 regions
    regions = [0.25, 0.75, 1.5]
    h = np.zeros(N)
    h[:int(N*0.25)] = 1.2
    h[int(N*0.25):int(N*0.75)] = 0.4
    h[int(N*0.75):int(N*1.5)] = 0.9
    h[int(N*1.5):] = -0.3
    h = np.clip(h, 0, 3)
    h = h / (np.sum(h) * domain + 1e-10)
    constructions['pw4'] = h
    
    return {"constructions": constructions, "num_constructions": 10}