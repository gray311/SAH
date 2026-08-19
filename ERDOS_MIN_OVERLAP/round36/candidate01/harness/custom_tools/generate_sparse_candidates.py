def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    cand1 = np.zeros(N)
    cand1[0:4] = 1.0
    cand1[361:365] = 1.0
    cand1 = cand1 * (1.0 / (8 * dx))
    
    cand2 = np.zeros(N)
    cand2[0:3] = 1.0
    cand2[400:403] = 1.0
    cand2[797:800] = 1.0
    cand2 = cand2 * (1.0 / (9 * dx))
    
    cand3 = np.zeros(N)
    cand3[0:5] = 1.0
    cand3[600:605] = 1.0
    cand3 = cand3 * (1.0 / (10 * dx))
    
    cand4 = np.zeros(N)
    cand4[200:400] = 1.0
    cand4 = cand4 * (1.0 / (200 * dx))
    
    cand5 = np.zeros(N)
    cand5[0] = 1.0
    cand5[300] = 1.0
    cand5[400] = 1.0
    cand5[500] = 1.0
    cand5[700] = 1.0
    cand5 = cand5 * (1.0 / (5 * dx))
    
    return {"cand1": cand1, "cand2": cand2, "cand3": cand3, "cand4": cand4, "cand5": cand5, "note": "Sparse step functions with integral equals 1"}