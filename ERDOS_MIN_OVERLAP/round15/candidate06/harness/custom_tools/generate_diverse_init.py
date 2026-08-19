def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    rng = np.random.default_rng(123)
    constructions = {}
    
    # Golomb ruler for 5 marks: [0, 1, 4, 9, 11] -> scale to [0,2]
    marks = np.array([0.0, 0.5, 1.6, 3.75, 4.4]) * 0.444  # scaled to [0,2]
    marks = marks / marks.max() * 2.0
    marks = marks[:5]
    weights = np.array([1.5, 1.2, 1.0, 0.8, 0.6])
    h_pattern = np.zeros(N)
    for m, w in zip(marks, weights):
        h_pattern += w * np.exp(-((np.arange(N) - m * N / 2) / (N * 0.15))**2)
    h_pattern = h_pattern / (np.sum(h_pattern) * dx + 1e-10)
    constructions['golomb_5'] = h_pattern
    
    # Bipartite: high on [0,a] U [a,2-a], low on [2-a,2]
    a = 0.6
    h_pattern = np.ones(N)
    start_idx = int(N * a / 2)
    end_idx = int(N * (2-a)/2)
    h_pattern[start_idx:end_idx] = -2.0
    h_pattern = np.clip(h_pattern, -5, 5)
    constructions['bipartite'] = h_pattern
    
    # Triple-peaked: three narrow peaks
    peaks = [0.4, 1.0, 1.6]
    bw = 0.12
    h_pattern = np.zeros(N)
    for p in peaks:
        h_pattern += 8.0 * np.exp(-((np.arange(N) - p * N / 2) / (N * bw / 2))**2)
    h_pattern = np.clip(h_pattern, 0, 10)
    constructions['triple_peaked'] = h_pattern
    
    # Asymmetric triangular: high on [0,0.5), medium on [0.5,1.5), low on [1.5,2]
    h_pattern = np.zeros(N)
    h_pattern[:int(N*0.5)] = 8.0
    h_pattern[int(N*0.5):int(N*1.5)] = 3.0
    h_pattern[int(N*1.5):] = -1.0
    constructions['asymmetric_triangular'] = h_pattern
    
    return {"constructions": constructions, "num_constructions": 4}