def run(ctx, args):
    import numpy as np
    num_candidates = args.get("num_candidates", 5)
    pattern_types = args.get("pattern_types", ["uniform", "bipartite", "multi_modal", "golomb", "sinusoidal"])
    
    candidates = []
    
    for i in range(min(num_candidates, len(pattern_types))):
        pattern = pattern_types[i]
        N = 800
        x = np.linspace(0, 2, N+1)[1:]  # 800 intervals, 800 points
        
        if pattern == "uniform":
            h = np.full(N, 0.5)  # 0.5*2 = 1.0 integral
            
        elif pattern == "bipartite":
            # h=1 for x<1, h=0 for x>=1
            h = np.where(x < 1.0, 1.0, 0.0)
            
        elif pattern == "multi_modal":
            # Three peaks of width 1/3 each
            # Peak centers at 0.4, 1.0, 1.6
            h = np.zeros(N)
            for center in [0.4, 1.0, 1.6]:
                half_width = 1/9  # 1/3 divided into 3 peaks
                mask = (x >= center - half_width) & (x < center + half_width)
                h[mask] = 1.0
            
        elif pattern == "golomb":
            # 5 marks at [0.0, 0.4, 0.8, 1.2, 1.6] with width 0.2 each
            marks = np.array([0.0, 0.4, 0.8, 1.2, 1.6])
            half_width = 0.1
            h = np.zeros(N)
            for m in marks:
                mask = (x >= m - half_width) & (x < m + half_width)
                h[mask] = 1.0
            
        elif pattern == "sinusoidal":
            # Peaks at maxima of sin(2πx): x = 0.25, 0.75, 1.25, 1.75
            peaks = np.array([0.25, 0.75, 1.25, 1.75])
            half_width = 0.15  # Adjust to get integral=1
            h = np.zeros(N)
            for p in peaks:
                mask = (x >= p - half_width) & (x < p + half_width)
                h[mask] = 1.0
        
        # Normalize to ensure integral=1
        h = np.clip(h, 0.0, 1.0)
        integral = np.sum(h) * (2.0 / N)
        if abs(integral - 1.0) > 1e-4:
            h = h / integral
        
        h = np.array([float(x) for x in h])
        candidates.append(h)
    
    return {"candidates": [c.tolist() for c in candidates]}