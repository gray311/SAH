def run(ctx, args):
    import numpy as np
    N = ctx.get_best_program() != None and 800
    if N is None:
        N = 800
    domain = 2.0
    dx = domain / N
    candidates = []
    
    # Candidate 1: Bimodal with adjustable separation
    for sep in [0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]:
        h = np.zeros(N)
        peak_width = 0.15
        for i in range(N):
            x = i * dx
            if (x >= sep - 0.075) and (x < sep + 0.075):
                h[i] = 1.0
            elif (x >= 1.0 - sep) and (x < 1.0 - sep + 0.075):
                h[i] = 1.0
        integral = h.sum() * dx
        if abs(integral - 1.0) < 0.3:
            h_norm = h * (1.0 / (h.sum() * dx))
            candidates.append((h_norm, f"bimodal_sep_{sep:.2f}", integral))
    
    # Candidate 2: Tripeak pattern
    x = np.linspace(0, domain, N)
    for centers in [(0.2, 0.5, 0.8), (0.15, 0.5, 0.85), (0.1, 0.5, 0.9), (0.15, 0.45, 0.85)]:
        h = np.zeros(N)
        for c in centers:
            for i in range(N):
                if abs((i*dx) - c) < 0.12:
                    h[i] = 1.0
        integral = h.sum() * dx
        if abs(integral - 1.0) < 0.3:
            h_norm = h * (1.0 / (h.sum() * dx))
            candidates.append((h_norm, f"tripeak_{centers}", integral))
    
    # Candidate 3: Periodic 2-period pattern with noise
    x = np.linspace(0, domain, N)
    periodic = np.zeros(N)
    for i in range(N):
        if x[i] < 0.5:
            periodic[i] = 1.0 + np.random.normal(0, 0.05)
        else:
            periodic[i] = 0.0 + np.random.normal(0, 0.05)
    periodic = np.clip(periodic, 0, 1)
    integral = periodic.sum() * dx
    if abs(integral - 1.0) < 0.2:
        periodic_norm = periodic * (1.0 / (periodic.sum() * dx))
        candidates.append((periodic_norm, "periodic_2_noise", integral))
    
    # Candidate 4: Golomb ruler inspired (5 marks)
    marks = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
    kernel_widths = np.array([0.08, 0.06, 0.08, 0.06, 0.08])
    h = np.zeros(N)
    for mark, kw in zip(marks, kernel_widths):
        for i in range(N):
            if abs((i*dx) - mark) < kw * 0.45:
                h[i] = 1.0
    integral = h.sum() * dx
    if abs(integral - 1.0) < 0.3:
        h_norm = h * (1.0 / (h.sum() * dx))
        candidates.append((h_norm, "golomb_5", integral))
    
    # Candidate 5: Narrow bimodal
    for sep in [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65]:
        h = np.zeros(N)
        bw = 0.08
        for i in range(N):
            x = i * dx
            if (x >= sep - bw*0.5) and (x < sep + bw*0.5):
                h[i] = 1.0
            elif (x >= 1.0 - sep) and (x < 1.0 - sep + bw*0.5):
                h[i] = 1.0
        integral = h.sum() * dx
        if abs(integral - 1.0) < 0.3:
            h_norm = h * (1.0 / (h.sum() * dx))
            candidates.append((h_norm, f"narrow_bimodal_sep_{sep:.2f}", integral))
    
    return {"candidates": candidates[:15], "count": len(candidates)}