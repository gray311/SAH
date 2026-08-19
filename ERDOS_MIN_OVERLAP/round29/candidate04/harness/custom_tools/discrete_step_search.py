def run(ctx, args):
    import numpy as np
    N = args.get("num_steps", 5)
    domain = 2.0
    dx = domain / N
    
    def compute_c5(h_arr):
        h_padded = np.pad(h_arr, (0, N))
        j_padded = np.pad(1.0 - h_arr, (0, N))
        corr = np.fft.ifft(np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))).real
        return np.max(corr * dx)
    
    def normalize_and_clip(h_arr):
        h_norm = h_arr / (np.sum(h_arr) * dx)
        h_norm = np.clip(h_norm, 0.001, 1.0)
        h_norm = h_norm / (np.sum(h_norm) * dx)
        return h_norm
    
    candidates = []
    
    # Pattern 1: Single step up at position 0.5
    h1 = np.zeros(N)
    h1[:int(N*0.5)] = 1.0
    h1 = normalize_and_clip(h1)
    candidates.append({"h": h1.tolist(), "c5_bound": float(compute_c5(h1)), "pattern": "single_up_0.5"})
    
    # Pattern 2: Single step up at position 0.3
    h2 = np.zeros(N)
    h2[:int(N*0.3)] = 1.0
    h2 = normalize_and_clip(h2)
    candidates.append({"h": h2.tolist(), "c5_bound": float(compute_c5(h2)), "pattern": "single_up_0.3"})
    
    # Pattern 3: Single step down at position 0.7
    h3 = np.zeros(N)
    h3[int(N*0.7):] = 1.0
    h3 = normalize_and_clip(h3)
    candidates.append({"h": h3.tolist(), "c5_bound": float(compute_c5(h3)), "pattern": "single_down_0.7"})
    
    # Pattern 4: Up-down (high at [0,a], low at [a,1-a], high at [1-a,1])
    h4 = np.zeros(N)
    h4[:int(N*0.3)] = 1.0
    h4[int(N*0.3):int(N*0.7)] = 0.5
    h4[int(N*0.7):] = 1.0
    h4 = normalize_and_clip(h4)
    candidates.append({"h": h4.tolist(), "c5_bound": float(compute_c5(h4)), "pattern": "up_down"})
    
    # Pattern 5: Multi-step (num_steps intervals with varying heights)
    step_heights = [0.8, 1.0, 0.6, 1.0, 0.9]  # Sum should be 1 when normalized
    h5 = np.zeros(N)
    for i, height in enumerate(step_heights):
        start_idx = int(i * N / len(step_heights))
        end_idx = int((i+1) * N / len(step_heights))
        h5[start_idx:end_idx] = height
    h5 = normalize_and_clip(h5)
    candidates.append({"h": h5.tolist(), "c5_bound": float(compute_c5(h5)), "pattern": f"multi_step_{N}"})
    
    # Pattern 6: Up-down with 3 steps
    h6 = np.zeros(N)
    h6[:int(N*0.25)] = 0.0
    h6[int(N*0.25):int(N*0.5)] = 1.0
    h6[int(N*0.5):int(N*0.75)] = 0.0
    h6[int(N*0.75):] = 1.0
    h6 = normalize_and_clip(h6)
    candidates.append({"h": h6.tolist(), "c5_bound": float(compute_c5(h6)), "pattern": "up_down_3step"})
    
    return {"candidates": candidates, "num_candidates": len(candidates)}
