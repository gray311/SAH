def run(ctx, args):
    import numpy as np
    grid_size = args.get("grid_size", 30)
    N = grid_size
    domain = 2.0
    dx = domain / N
    
    def compute_c5(h_arr):
        h_padded = np.pad(h_arr, (0, N))
        j_padded = np.pad(1.0 - h_arr, (0, N))
        corr = np.fft.ifft(np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))).real
        return np.max(corr * dx)
    
    candidates = []
    
    # Pattern 1: Binary step at different locations
    for a in [0.2, 0.4, 0.6, 0.8]:
        h = np.zeros(N)
        h[int(a * N)] = 1.0
        integral = np.sum(h) * dx
        if abs(integral - 1.0) < 0.01:
            h = h / integral
        candidates.append({"h": h.tolist(), "c5_bound": float(compute_c5(h)), "pattern": f"binary_step_a{a}"})
    
    # Pattern 2: Uniform step (constant)
    h_uniform = np.ones(N) * 0.5
    candidates.append({"h": h_uniform.tolist(), "c5_bound": float(compute_c5(h_uniform)), "pattern": "uniform_0.5"})
    
    # Pattern 3: Three-level step
    h_3level = np.zeros(N)
    h_3level[:int(0.3*N)] = 1.0
    h_3level[int(0.3*N):int(0.7*N)] = 0.5
    h_3level[int(0.7*N):] = 0.0
    candidates.append({"h": h_3level.tolist(), "c5_bound": float(compute_c5(h_3level)), "pattern": "three_level"})
    
    # Pattern 4: Asymmetric with integral constraint
    h_asym = np.zeros(N)
    h_asym[:int(0.5*N)] = 1.0
    h_asym[int(0.5*N):] = 0.0
    candidates.append({"h": h_asym.tolist(), "c5_bound": float(compute_c5(h_asym)), "pattern": "asymmetric_50"})
    
    # Pattern 5: Central step
    h_central = np.zeros(N)
    h_central[int(0.25*N):int(0.75*N)] = 1.0
    candidates.append({"h": h_central.tolist(), "c5_bound": float(compute_c5(h_central)), "pattern": "central_step"})
    
    return {"candidates": candidates, "grid_size": grid_size}
