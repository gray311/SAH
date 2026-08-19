def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    constructions = {}
    
    # 2-segment: h=5 on [0,1], h=0 on [1,2]
    h2_seg = np.zeros(N)
    h2_seg[:int(N)] = 5.0
    constructions['seg2_1half'] = h2_seg
    
    # 3-segment patterns
    h3_seg = np.zeros(N)
    h3_seg[:int(N*0.4)] = 5.0
    h3_seg[int(N*0.4):int(N*1.0)] = 2.0
    constructions['seg3_04_1'] = h3_seg
    
    h3b = np.zeros(N)
    h3b[:int(N*0.5)] = 5.0
    h3b[int(N*0.5):int(N*1.5)] = 2.0
    constructions['seg3_05_15'] = h3b
    
    # 4-segment asymmetric
    h4 = np.zeros(N)
    h4[:int(N*0.3)] = 5.0
    h4[int(N*0.3):int(N*0.7)] = 3.0
    h4[int(N*0.7):int(N*1.2)] = 1.5
    h4[int(N*1.2):] = 0.0
    constructions['seg4_asym'] = h4
    
    # 4-segment more balanced
    h4b = np.zeros(N)
    h4b[:int(N*0.25)] = 5.0
    h4b[int(N*0.25):int(N*0.5)] = 3.0
    h4b[int(N*0.5):int(N*1.5)] = 1.5
    h4b[int(N*1.5):int(N*1.75)] = 0.5
    h4b[int(N*1.75):] = 0.0
    constructions['seg4_balanced'] = h4b
    
    # Single peak
    peak_idx = int(N * 0.5)
    h_peak = np.zeros(N)
    for i in range(N):
        h_peak[i] = 5.0 * np.exp(-abs(i - peak_idx) / (N * 0.1))
    constructions['peak_half'] = h_peak
    
    return {"constructions": constructions, "num_constructions": len(constructions)}
