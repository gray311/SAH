def run(ctx, args):
    import numpy as np
    np.random.seed(42)
    N = 800
    domain = 2.0
    dx = domain / N
    constructions = {}
    
    # Pattern 1: Binary step
    a = 1.0 / 0.6
    h_pat1 = np.zeros(N)
    h_pat1[:int(N*a)] = 6.0  # High value before sigmoid
    constructions['binary_step'] = h_pat1
    
    # Pattern 2: 3-part piecewise
    a, b = 0.4, 1.2
    h_pat2 = np.zeros(N)
    h_pat2[:int(N*a)] = 5.0
    h_pat2[int(N*a):int(N*b)] = 2.0
    h_pat2[int(N*b):] = -1.0
    constructions['piecewise_3'] = h_pat2
    
    # Pattern 3: Asymmetric trapezoid
    h_pat3 = np.zeros(N)
    h_pat3[:int(N*0.4)] = 8.0
    h_pat3[int(N*0.4):int(N*1.2)] = 3.0
    h_pat3[int(N*1.2):] = -1.0
    constructions['asymmetric_trap'] = h_pat3
    
    # Pattern 4: Bimodal
    h_pat4 = np.zeros(N)
    h_pat4[int(N*0.3*1000/2):int(N*0.6*1000/2)] = 10.0
    h_pat4[int(N*1.4*1000/2):int(N*1.7*1000/2)] = 10.0
    constructions['bimodal'] = h_pat4
    
    # Pattern 5: Sparse 3-peak
    h_pat5 = np.zeros(N)
    h_pat5[int(N*0.4*1000/2):int(N*0.55*1000/2)] = 12.0
    h_pat5[int(N*0.9*1000/2):int(N*1.05*1000/2)] = 12.0
    h_pat5[int(N*1.5*1000/2):int(N*1.65*1000/2)] = 12.0
    constructions['sparse_3peak'] = h_pat5
    
    return {"constructions": constructions, "num_constructions": 5}
