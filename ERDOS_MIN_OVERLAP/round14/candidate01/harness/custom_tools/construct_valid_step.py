def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    h_values = None
    pattern = args.get("pattern", "two_step")
    target_integral = args.get("integral", 1.0)
    
    if pattern == "two_step":
        # h = 1 on [0, a), 0 on [a, 2), integral = a = target_integral
        a = target_integral
        h_values = np.zeros(N)
        h_values[:int(a * N)] = 1.0
        
    elif pattern == "three_step":
        # h = 1 on [0, a1), 0.5 on [a1, a2), 0 on [a2, 2)
        # integral = a1*1 + (a2-a1)*0.5 = target_integral
        # Choose a1 = 0.4, solve for a2
        a1 = 0.4
        a2 = target_integral - a1 + a1 * 0.5
        h_values = np.zeros(N)
        h_values[:int(a1 * N)] = 1.0
        h_values[int(a1 * N):int(a2 * N)] = 0.5
        
    elif pattern == "five_step":
        # Golomb ruler positions scaled to [0,2]: [0, 0.5, 1.2, 1.6, 2.0]
        # Heights: 1.5, 1.2, 1.0, 0.8, 0.6 (weights)
        # Each pulse width = 0.15
        positions = [0.0, 0.5, 1.2, 1.6, 2.0]
        heights = [1.5, 1.2, 1.0, 0.8, 0.6]
        widths = [0.1, 0.1, 0.15, 0.15, 0.05]
        
        h_values = np.zeros(N)
        for pos, height, width in zip(positions, heights, widths):
            start = int(pos * N)
            end = int((pos + width) * N)
            h_values[start:end] = height
    
    else:
        # Default: uniform distribution (h=0.5 everywhere, integral=1.0)
        h_values = np.full(N, 0.5)
    
    # Normalize to exact integral = target_integral
    current_integral = np.sum(h_values) * (domain / N)
    if current_integral > 0:
        h_values = h_values * target_integral / current_integral
    
    return {"type": pattern, "h_values": h_values.tolist(), 
            "integral": float(current_integral * target_integral / np.sum(h_values) * (domain/N))}
