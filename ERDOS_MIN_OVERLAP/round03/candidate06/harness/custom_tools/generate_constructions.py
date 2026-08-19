def run(ctx, args):
    import numpy as np
    N_str = ctx.get_program()
    if 'num_intervals' in str(N_str):
        N = 800
    else:
        try:
            N = int(N_str)
        except ValueError:
            N = 800
    domain = 2.0
    x = np.linspace(0, domain, N)
    constructions = {}
    
    # Asymmetric bimodal (LEFT narrower, target: better overlap)
    a1, a2 = 0.25, 1.75
    bw1, bw2 = 0.12, 0.18
    h = np.exp(-((x-a1)/bw1)**2 * 25) + np.exp(-((x-a2)/bw2)**2 * 25)
    h = h / h.sum() * N  # normalize integral to 1
    constructions['asym_bimodal'] = h
    
    # Symmetric bimodal
    bw = 0.15
    h = np.exp(-((x-0.25)/bw)**2 * 25) + np.exp(-((x-1.75)/bw)**2 * 25)
    h = h / h.sum() * N
    constructions['sym_bimodal'] = h
    
    # 4-level triangular
    x_b = np.linspace(0, 2, N)
    levels = np.array([0.2, 0.5, 0.7, 0.9])
    phases = np.array([0.0, 0.5, 0.75, 1.0])
    h_tri = np.zeros(N)
    for i in range(len(phases)-1):
        p1, p2 = phases[i], phases[i+1]
        mask = (x_b >= p1) & (x_b < p2)
        h_tri[mask] = levels[i]
    h_tri = h_tri / h_tri.sum() * N
    constructions['triangular_4'] = h_tri
    
    # Periodic folded
    h_per = 1.0 / (1.0 + np.exp(-10 * ((x_b - 0.5) % 1.0 - 0.25)))
    h_per = h_per / h_per.sum() * N
    constructions['periodic'] = h_per
    
    # Golomb 7 marks: [0,1,4,9,11,12,13] scaled
    marks = np.array([0.0, 0.1905, 0.4762, 0.9524, 1.1429, 1.1905, 1.1952]) * 2.0
    h_gol = np.zeros(N)
    for m in marks:
        h_gol += np.exp(-((x_b - m)/0.08)**2 * 30)
    h_gol = h_gol / h_gol.sum() * N
    constructions['golomb_7'] = h_gol
    
    return {"constructions": constructions}