def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    constructions = []
    
    # 2-block: a on [0,x1), 0 on [x1,2], where a*x1 = 1
    for a in [0.5, 0.6, 0.7, 0.8]:
        x1 = 1.0 / a
        if x1 < 2.0:
            h = np.zeros(N)
            h[:int(x1*N)] = a
            constructions.append(("2block_a" + str(a), h))
    
    # 3-block: h1 on [0,x1), h2 on [x1,x2), 0 on [x2,2)
    patterns = [
        ((0.5, 0.8), 1.0, 0.5),
        ((0.4, 0.7), 1.0, 0.5),
        ((0.3, 0.6), 1.0, 0.5),
        ((0.4, 0.9), 0.8, 0.4),
        ((0.5, 1.0), 0.6, 0.3),
    ]
    for (x1, x2), h1, h2 in patterns:
        h_arr = np.zeros(N)
        h_arr[:int(x1*N)] = h1
        h_arr[int(x1*N):int(x2*N)] = h2
        total = h_arr.sum() * dx
        if total > 0:
            h_arr = h_arr / total
        constructions.append(("3block_x1" + str(x1), h_arr))
    
    # 4-block asymmetric
    h_arr = np.zeros(N)
    h_arr[:int(0.4*N)] = 1.0
    h_arr[int(0.4*N):int(1.0*N)] = 0.5
    h_arr[int(1.0*N):int(1.5*N)] = 0.3
    total = h_arr.sum() * dx
    if total > 0:
        h_arr = h_arr / total
    constructions.append(("4block_asym", h_arr))
    
    # Support-split variant
    h_arr = np.zeros(N)
    h_arr[:int(0.2*N)] = 0.5
    h_arr[int(0.2*N):] = 1.0
    total = h_arr.sum() * dx
    if total > 0:
        h_arr = h_arr / total
    constructions.append(("support_split", h_arr))
    
    return {"constructions": dict(constructions), "num_constructions": len(constructions)}
