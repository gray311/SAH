def run(ctx, args):
    import random
    import numpy as np
    
    N = 800
    domain = 2.0
    dx = domain / N
    
    # Ensure integral = 1: need exactly 2.0/N * num_on_intervals = 1.0
    # So num_on_intervals * dx = 1.0 => num_on_intervals = N/2 = 400
    num_on = int(args.get('num_on_intervals', N/2))
    num_samples = args.get('num_samples', 5)
    strategy = args.get('strategy', 'uniform_k_widths')
    
    candidates = []
    
    if strategy == 'uniform_k_widths':
        # Select num_on random positions out of N
        for _ in range(num_samples):
            on_positions = set(random.sample(range(N), num_on))
            h = np.zeros(N)
            for i in on_positions:
                h[i] = 1.0
            candidates.append(h)
            
    elif strategy == 'clustered_peaks':
        # Concentrate on intervals in few regions
        for _ in range(num_samples):
            # Pick 2-4 clusters, each with 100-200 intervals
            num_clusters = random.randint(2, 4)
            total_needed = num_on
            cluster_sizes = np.random.randint(50, 200, size=num_clusters)
            # Adjust to hit exact count
            if cluster_sizes.sum() != total_needed:
                diff = total_needed - cluster_sizes.sum()
                cluster_sizes[0] += diff
            sizes = cluster_sizes.tolist()
            
            h = np.zeros(N)
            for j, size in enumerate(sizes):
                center = random.randint(0, N-1)
                start = max(0, center - size//2)
                end = min(N, center + size//2 + 1)
                h[start:end] = 1.0
            candidates.append(h)
            
    else:  # alternating
        # Short alternating on/off pattern
        for _ in range(num_samples):
            pattern_len = random.randint(20, 100)
            pattern = []
            for _ in range(N // pattern_len):
                pattern.extend([1] * (num_on // (N // pattern_len) // 2))
                pattern.extend([0] * (num_on // (N // pattern_len) // 2))
            
            h = np.zeros(N)
            for i, val in enumerate(pattern):
                if i < N:
                    h[i] = val
            # Pad or trim to exactly N
            if len(pattern) < N:
                while len(pattern) < N:
                    pattern.extend([0])
            h = h[:N]
            candidates.append(h)
    
    # Convert to string format for solver
    h_strings = [", ".join([str(int(x)) for x in c]) for c in candidates]
    return {"candidates": h_strings, "num_generated": len(candidates)}
