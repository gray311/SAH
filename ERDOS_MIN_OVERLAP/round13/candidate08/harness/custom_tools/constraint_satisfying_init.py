def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    rng = np.random.default_rng(42)

    constructions = {}

    # Pattern 1: Uniform on [0,1], zero on [1,2]
    h1 = np.zeros(N)
    h1[:int(N/2)] = 1.0
    h1[int(N/2):] = 0.0
    h1[:int(N*0.2)] = 0.5 + 0.5 * np.sin(np.pi * np.arange(int(N*0.2)) / int(N*0.2))
    h1[int(N*0.8):] = 0.5 + 0.5 * np.sin(np.pi * (np.arange(int(N*0.8), N) - int(N*0.8)) / int(N*0.2))
    h1 = h1 / (np.sum(h1) * dx)
    latent1 = np.log(h1 / (1 - h1 + 1e-10))
    constructions['uniform_half'] = latent1

    # Pattern 2: Two equal halves with a dip
    h2 = np.ones(N) * 0.5
    h2[int(N*0.2):int(N*0.8)] = 0.0
    h2 = h2 / (np.sum(h2) * dx)
    latent2 = np.log(h2 / (1 - h2 + 1e-10))
    constructions['dip'] = latent2

    # Pattern 3: Three equal thirds
    h3 = np.zeros(N)
    h3[int(N/3):int(N*2/3)] = 1.0
    h3 = h3 / (np.sum(h3) * dx)
    latent3 = np.log(h3 / (1 - h3 + 1e-10))
    constructions['third'] = latent3

    # Pattern 4: Quadratic-like
    x = np.linspace(0, 2, N)
    h4 = 1 - (x - 1)**2
    h4 = np.maximum(h4, 0)
    h4 = h4 / (np.sum(h4) * dx)
    latent4 = np.log(h4 / (1 - h4 + 1e-10))
    constructions['quadratic'] = latent4

    return {"constructions": constructions, "num_constructions": 4}
