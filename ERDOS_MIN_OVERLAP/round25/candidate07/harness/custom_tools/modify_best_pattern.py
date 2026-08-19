def run(ctx, args):
    import numpy as np
    
    h_input = np.array(args.get('h', []))
    N = len(h_input)
    if N == 0:
        return {"candidates": [], "num_candidates": 0}
    domain = 2.0
    dx = domain / N
    
    temp = float(args.get('temperature', 0.5))
    
    # Variant 1: Gaussian smoothing
    sigma = N * 0.15
    kernel = np.exp(-0.5 * ((np.arange(N)[:,None] - np.arange(N)[None,:]) / sigma)**2)
    kernel_sum = kernel.sum(axis=1, keepdims=True)
    kernel_sum = np.where(kernel_sum == 0, 1.0, kernel_sum)
    kernel = kernel / kernel_sum
    h_gaussian = np.zeros(N)
    for i in range(N):
        h_gaussian += h_input[i] * kernel[i]
    h_gaussian = np.clip(h_gaussian, 0.01, 1.0)
    h_gaussian = h_gaussian / np.sum(h_gaussian) * (1.0 / dx)
    h_gaussian = np.clip(h_gaussian, 0.01, 1.0)
    h_gaussian = h_gaussian / np.sum(h_gaussian) * (1.0 / dx)
    
    # Variant 2: Peak sharpening
    h_sharp = h_input.copy()
    h_sharp[1:N-1] = 1.5 * h_sharp[1:N-1] + 0.1 * h_input[0:N-2] - 0.1 * h_input[2:N]
    h_sharp = np.clip(h_sharp, 0.01, 5.0)
    h_sharp = np.exp(h_sharp) / (np.sum(np.exp(h_sharp)) + 1e-10)
    h_sharp = h_sharp / np.sum(h_sharp) * (1.0 / dx)
    h_sharp = np.clip(h_sharp, 0.01, 1.0)
    h_sharp = h_sharp / np.sum(h_sharp) * (1.0 / dx)
    
    # Variant 3: Phase modulation
    h_phase = h_input + 0.3 * (np.sin(2 * np.pi * np.arange(N) / N * 3) + 
                               np.sin(2 * np.pi * np.arange(N) / N * 5))
    h_phase = np.clip(h_phase, -1.0, 5.0)
    h_phase = np.exp(h_phase) / (np.sum(np.exp(h_phase)) + 1e-10)
    h_phase = h_phase / np.sum(h_phase) * (1.0 / dx)
    h_phase = np.clip(h_phase, 0.01, 1.0)
    h_phase = h_phase / np.sum(h_phase) * (1.0 / dx)
    
    # Compute analytical c5_bound for each
    def compute_c5(h_arr):
        j_val = 1.0 - h_arr
        h_padded = np.pad(h_arr, (0, N))
        j_padded = np.pad(j_val, (0, N))
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        c5 = np.max(correlation * dx)
        return float(c5)
    
    results = [
        {"h": h_gaussian.tolist(), "integral": float(np.sum(h_gaussian) * dx),
         "c5_bound": compute_c5(h_gaussian), "modification_type": "gaussian_smoothing"},
        {"h": h_sharp.tolist(), "integral": float(np.sum(h_sharp) * dx),
         "c5_bound": compute_c5(h_sharp), "modification_type": "peak_sharpening"},
        {"h": h_phase.tolist(), "integral": float(np.sum(h_phase) * dx),
         "c5_bound": compute_c5(h_phase), "modification_type": "phase_modulation"}
    ]
    
    return {"candidates": results, "num_candidates": 3}