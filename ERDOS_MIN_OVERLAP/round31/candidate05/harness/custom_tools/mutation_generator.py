def run(ctx, args):
    import math
    
    mutation_type = args.get("mutation_type", "bipartite")
    params = args.get("params", {})
    num_intervals = args.get("num_intervals", 800)
    
    dx = 2.0 / num_intervals
    h = [0.0] * num_intervals
    
    if mutation_type == "bipartite":
        t = 1.0
        for i in range(num_intervals):
            x = i * dx
            if x < t:
                h[i] = 1.0
            else:
                h[i] = 0.0
    
    elif mutation_type == "multi_modal":
        centers = params.get("centers", [0.4, 1.0, 1.6])
        for c in centers:
            c_idx = int(c / dx)
            for i in range(max(0, c_idx - 5), min(num_intervals, c_idx + 6)):
                x = i * dx
                dist = abs(x - c)
                h[i] += math.exp(-dist / 0.1)
        
        # Normalize
        integral = sum(h) * dx
        if integral > 0:
            h = [v / integral for v in h]
    
    elif mutation_type == "spread_peaks":
        num_peaks = params.get("num_peaks", 5)
        for i in range(num_peaks):
            c = i * (2.0 / num_peaks)
            c_idx = int(c / dx)
            for j in range(max(0, c_idx - 2), min(num_intervals, c_idx + 3)):
                h[j] = 1.0
        
        # Normalize
        integral = sum(h) * dx
        if integral > 0:
            h = [v / integral for v in h]
    
    return {"h": h, "mutation_type": mutation_type}
