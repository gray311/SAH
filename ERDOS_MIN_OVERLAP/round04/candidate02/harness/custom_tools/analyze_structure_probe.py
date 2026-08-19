def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    constructions = {}
    x = np.linspace(0, domain, N)
    
    # periodic_1: h=1 on [0,1], h=0 on (1,2] - integral=1 exactly
    h_periodic_1 = np.zeros(N)
    h_periodic_1[:500] = 1.0
    constructions["periodic_1"] = h_periodic_1
    
    # periodic_2: h=1 on [0,0.5] U [1,1.5], h=0 elsewhere - integral=1
    h_periodic_2 = np.zeros(N)
    mask1 = (x >= 0) & (x < 0.5)
    mask2 = (x >= 1) & (x < 1.5)
    h_periodic_2[mask1] = 1.0
    h_periodic_2[mask2] = 1.0
    constructions["periodic_2"] = h_periodic_2
    
    # bimodal_tight: Two very narrow peaks at 0.25 and 0.75, normalized to integral=1
    h_bimodal = np.zeros(N)
    sigma = 0.08
    h_bimodal += np.exp(-((x - 0.25) / sigma)**2 * 50)
    h_bimodal += np.exp(-((x - 0.75) / sigma)**2 * 50)
    integral_h = np.sum(h_bimodal) * dx
    if integral_h > 0:
        h_bimodal = h_bimodal / integral_h
    constructions["bimodal_tight"] = h_bimodal
    
    # triangular_3: Three-level step, normalized to integral=1
    h_triangular = np.zeros(N)
    h_triangular[200:400] = 0.5
    h_triangular[400:800] = 1.0
    integral_h = np.sum(h_triangular) * dx
    if integral_h > 0:
        h_triangular = h_triangular / integral_h
    constructions["triangular_3"] = h_triangular
    
    # golomb_5: Based on Golomb ruler positions, normalized to integral=1
    golomb_positions = np.array([0.0, 0.5, 1.2, 1.6, 1.8])
    golomb_weights = np.array([1.0, 1.0, 0.8, 0.8, 1.0])
    h_golomb = np.zeros(N)
    for pos, weight in zip(golomb_positions, golomb_weights):
        h_golomb += weight * np.exp(-((x - pos) / 0.12)**2 * 60)
    integral_h = np.sum(h_golomb) * dx
    if integral_h > 0:
        h_golomb = h_golomb / integral_h
    constructions["golomb_5"] = h_golomb
    
    return {"constructions": constructions, "construction_names": list(constructions.keys())}
