def run(ctx, args):
    import numpy as np
    max_c5 = args.get("max_c5_threshold", 0.375)
    
    N_probe = 50
    domain = 2.0
    dx = domain / N_probe
    
    latent = np.random.randn(N_probe) * 2.0
    lr = 0.1
    num_steps = 10
    
    for step in range(num_steps):
        h = 1.0 / (1.0 + np.exp(-latent))
        j = 1.0 - h
        h_pad = np.pad(h, (0, N_probe))
        j_pad = np.pad(j, (0, N_probe))
        H_fft = np.fft.fft(h_pad)
        J_fft = np.fft.fft(j_pad)
        corr = np.fft.ifft(H_fft * np.conj(J_fft)).real
        
        grad = np.zeros(N_probe)
        for i in range(N_probe):
            latent_plus = latent.copy()
            latent_minus = latent.copy()
            latent_plus[i] += 1e-3
            latent_minus[i] -= 1e-3
            
            h_plus = 1.0 / (1.0 + np.exp(-latent_plus))
            j_plus = 1.0 - h_plus
            h_pad_plus = np.pad(h_plus, (0, N_probe))
            j_pad_plus = np.pad(j_plus, (0, N_probe))
            corr_plus = np.fft.ifft(np.fft.fft(h_pad_plus) * np.conj(np.fft.fft(j_pad_plus))).real
            c5_plus = np.max(corr_plus * dx)
            
            h_minus = 1.0 / (1.0 + np.exp(-latent_minus))
            j_minus = 1.0 - h_minus
            h_pad_minus = np.pad(h_minus, (0, N_probe))
            j_pad_minus = np.pad(j_minus, (0, N_probe))
            corr_minus = np.fft.ifft(np.fft.fft(h_pad_minus) * np.conj(np.fft.fft(j_pad_minus))).real
            c5_minus = np.max(corr_minus * dx)
            
            grad[i] = (c5_plus - c5_minus) / 2e-3
        
        latent -= lr * grad
        latent = np.clip(latent, -10, 10)
    
    h = 1.0 / (1.0 + np.exp(-latent))
    h = np.clip(h, 0.001, 0.999)
    integral = np.sum(h) * dx
    if integral > 0:
        h = h / integral
    
    j = 1.0 - h
    h_pad = np.pad(h, (0, N_probe))
    j_pad = np.pad(j, (0, N_probe))
    H_fft = np.fft.fft(h_pad)
    J_fft = np.fft.fft(j_pad)
    corr = np.fft.ifft(H_fft * np.conj(J_fft)).real
    c5_bound = float(np.max(corr * dx))
    
    return {
        "h": h.tolist(),
        "integral": float(np.sum(h) * dx),
        "c5_bound": c5_bound,
        "N_probe": N_probe,
        "recommended": c5_bound < max_c5,
        "note": f"Coarse probe (N={N_probe}). Use evaluate_solution if c5<0.375."
    }
