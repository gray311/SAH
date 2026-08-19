def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    h_vectors = {}
    
    # Pattern 1: piecewise constant with 3 breakpoints
    h1 = np.zeros(N)
    h1[:int(N*0.25)] = 4.0
    h1[int(N*0.25):int(N*0.75)] = 0.5
    h1[int(N*0.75):] = 2.0
    total = np.sum(h1) * dx
    h1 = h1 / (total + 1e-10)
    h_vectors['piecewise_constant_3'] = h1
    
    # Pattern 2: Golomb ruler for 5 marks: [0, 1, 4, 9, 11] scaled to [0,2]
    marks = np.array([0.0, 0.5, 1.6, 3.75, 4.4]) * 0.4
    marks = marks[:5]
    h2 = np.zeros(N)
    for m in marks:
        h2 += 3.0 * np.exp(-((np.arange(N) - m * N / 2) / (N * 0.08))**2)
    total = np.sum(h2) * dx
    h2 = h2 / (total + 1e-10)
    h_vectors['golomb_5_marks'] = h2
    
    # Pattern 3: Golomb ruler for 7 marks
    marks7 = np.array([0.0, 0.4, 1.2, 2.8, 3.2, 4.8, 5.0]) * 0.4
    marks7 = marks7[:7]
    h3 = np.zeros(N)
    for m in marks7:
        h3 += 2.0 * np.exp(-((np.arange(N) - m * N / 2) / (N * 0.12))**2)
    total = np.sum(h3) * dx
    h3 = h3 / (total + 1e-10)
    h_vectors['golomb_7_marks'] = h3
    
    # Pattern 4: Asymmetric triangular
    h4 = np.zeros(N)
    h4[:int(N*0.3)] = 6.0
    h4[int(N*0.3):int(N*0.7)] = 1.5
    h4[int(N*0.7):] = 0.5
    total = np.sum(h4) * dx
    h4 = h4 / (total + 1e-10)
    h_vectors['asymmetric_triangular'] = h4
    
    # Pattern 5: Multi-peak with 3 peaks
    h5 = np.zeros(N)
    h5[int(N*0.1):int(N*0.35)] = 5.0
    h5[int(N*0.35):int(N*0.6)] = 3.0
    h5[int(N*0.6):int(N*0.85)] = 4.5
    total = np.sum(h5) * dx
    h5 = h5 / (total + 1e-10)
    h_vectors['multi_peak_3'] = h5
    
    return {"h_vectors": h_vectors, "num_patterns": 5}
