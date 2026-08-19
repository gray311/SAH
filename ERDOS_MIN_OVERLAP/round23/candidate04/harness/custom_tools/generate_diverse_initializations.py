def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    
    # Candidate 1: Sparse concentrated (all energy in [0, 0.6])
    sparse = np.zeros(N)
    sparse[:int(0.6*N)] = 3.5
    sparse[int(0.6*N):int(0.8*N)] = -2.0
    sparse[int(0.8*N):] = 2.0
    sparse += np.random.randn(N) * 0.3
    sparse = np.clip(sparse, -5, 5)
    
    # Candidate 2: Bimodal (two peaks separated)
    bimodal = np.zeros(N)
    center1 = int(0.35 * N)
    center2 = int(0.85 * N)
    w = max(1, N // 50)
    for c in [center1, center2]:
        for i in range(max(0, c-w), min(N, c+w+1)):
            bm = np.exp(-((i - c) / w)**2)
            bimodal[i] += 4.0 * bm
    bimodal += np.random.randn(N) * 0.3
    bimodal = np.clip(bimodal, -5, 5)
    
    # Candidate 3: Trimodal (three peaks)
    trimodal = np.zeros(N)
    for c in [int(0.3*N), int(0.7*N), int(1.3*N)]:
        w = max(1, N // 80)
        for i in range(max(0, c-w), min(N, c+w+1)):
            tm = np.exp(-((i - c) / w)**2)
            trimodal[i] += 4.0 * tm
    trimodal += np.random.randn(N) * 0.3
    trimodal = np.clip(trimodal, -5, 5)
    
    # Add noise for diversity
    sparse += np.random.randn(N) * 0.5
    bimodal += np.random.randn(N) * 0.5
    trimodal += np.random.randn(N) * 0.5
    
    # Wrap in dicts (optimizer expects latent vectors)
    return {
        "candidates": [
            {"latent": sparse.tolist(), "type": "sparse_concentrated"},
            {"latent": bimodal.tolist(), "type": "bimodal"},
            {"latent": trimodal.tolist(), "type": "trimodal"}
        ],
        "num_candidates": 3
    }
