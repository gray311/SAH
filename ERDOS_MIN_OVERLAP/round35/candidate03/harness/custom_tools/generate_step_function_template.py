def run(ctx, args):
    import json
    import random
    
    template = args.get("template_type", "three_peak")
    N = args.get("num_intervals", 800)
    domain = 2.0
    dx = domain / N
    
    h_vals = []
    
    if template == "bipartite":
        for i in range(N):
            x = i * dx
            h_vals.append(1.0 if x < 1.0 else 0.0)
    
    elif template == "two_peak":
        width = 30
        peak1_pos = int(N * 0.25)
        peak2_pos = int(N * 0.75)
        for i in range(N):
            x = i * dx
            d1 = abs(x - (peak1_pos * dx))
            d2 = abs(x - (peak2_pos * dx))
            if d1 < width * dx or d2 < width * dx:
                h_vals.append(min(1.0, 1.0 - d1/(width*dx)))
            else:
                h_vals.append(0.0)
    
    elif template == "three_peak":
        width = 25
        peak_positions = [int(N * i/6) for i in [1, 3, 5]]
        for i in range(N):
            x = i * dx
            min_d = min(abs(x - (p * dx)) for p in peak_positions)
            if min_d < width * dx:
                h_vals.append(min(1.0, 1.0 - min_d/(width*dx)))
            else:
                h_vals.append(0.0)
    
    elif template == "golomb":
        width = 20
        peak_positions = [0, int(N*2/3), int(N*4/3), N-1]
        for i in range(N):
            x = i * dx
            d = min(abs(x - (p * dx)) for p in peak_positions)
            if d < width * dx:
                h_vals.append(min(1.0, 1.0 - d/(width*dx)))
            else:
                h_vals.append(0.0)
    
    elif template == "broad_plateau":
        start = int(N * 0.2)
        end = int(N * 1.8)
        plateau_width = end - start
        height = 1.0 / plateau_width if plateau_width > 0 else 1.0
        for i in range(N):
            if start <= i < end:
                h_vals.append(height)
            else:
                h_vals.append(0.0)
    
    current_sum = sum(h_vals)
    if current_sum > 0 and N > 0:
        scale = 1.0 / current_sum
        h_vals = [v * scale for v in h_vals]
    
    h_vals = [max(0.0, min(1.0, v)) for v in h_vals]
    
    return {
        "template_type": template,
        "h_values": h_vals,
        "num_intervals": N,
        "domain": domain,
        "integral_check": sum(h_vals) / N * domain,
        "note": f"Generated {template} step function with {len(h_vals)} points"
    }
