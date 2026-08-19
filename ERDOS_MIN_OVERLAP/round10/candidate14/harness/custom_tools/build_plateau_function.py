def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    constructions = {}
    single = np.ones(N) * 0.5
    constructions['single_05'] = single
    for a in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
        L = 1.0
        b = (1.0 - a * L) / (domain - L)
        b_val = max(0.0, min(1.0, b))
        if abs(a - b_val) < 0.01:
            continue
        bimodal = np.concatenate([np.ones(int(L*N)) * a, np.ones(N - int(L*N)) * b_val])
        constructions['bimodal_' + str(int(a*100))] = bimodal
    spike = np.concatenate([np.ones(400), np.zeros(400)])
    constructions['spike_concentrated'] = spike
    spread1 = np.concatenate([np.ones(400) * 0.4, np.ones(400) * 0.6])
    constructions['spread_04_06'] = spread1
    spread2 = np.concatenate([np.ones(400) * 0.3, np.ones(400) * 0.7])
    constructions['spread_03_07'] = spread2
    return {"constructions": constructions}