def run(ctx, args):
    import numpy as np
    original_h = np.array(args.get('original_h', [1.0] * 100))
    N = len(original_h)
    dx = 2.0 / N
    
    def normalize_and_clip(h_arr):
        h_sum = np.sum(h_arr) * dx
        if h_sum < 1e-8:
            h_sum = 1e-8
        h_norm = h_arr / (h_sum * dx)
        h_norm = np.clip(h_norm, 0.001, 1.0)
        h_norm = h_norm / (np.sum(h_norm) * dx)
        return h_norm
    
    def compute_c5(h_arr):
        h_padded = np.pad(h_arr, (0, N))
        j_padded = np.pad(1.0 - h_arr, (0, N))
        corr = np.fft.ifft(np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))).real
        return float(np.max(corr * dx))
    
    candidates = []
    
    # Shift mutations (3 variants)
    for delta in [args.get('mutation_param', 0.1), -args.get('mutation_param', 0.1), 0.5]:
        h_shifted = original_h.copy()
        h_shifted = np.roll(h_shifted, -int(delta * N))
        h_shifted = normalize_and_clip(h_shifted)
        c5 = compute_c5(h_shifted)
        candidates.append({'h': h_shifted.tolist(), 'c5_bound': c5, 'type': f'shift_{delta:.2f}'})
    
    # Split mutation (split at 50% width)
    if np.sum(original_h > 0.1) > 10:
        nonzero = original_h > 0.1
        indices = np.where(nonzero)[0]
        if len(indices) > 1:
            mid = (indices[0] + indices[-1]) // 2
            h_split = original_h.copy()
            h_split[mid-5:mid+5] = 0.0
            h_split = normalize_and_clip(h_split)
            c5 = compute_c5(h_split)
            candidates.append({'h': h_split.tolist(), 'c5_bound': c5, 'type': 'split'})
    
    # Add peak mutation
    h_add = original_h.copy()
    center = N // 2
    width = 5
    h_add[center-3:center+4] += 3.0
    h_add = normalize_and_clip(h_add)
    c5 = compute_c5(h_add)
    candidates.append({'h': h_add.tolist(), 'c5_bound': c5, 'type': 'add_peak'})
    
    # Remove peak mutation
    h_remove = original_h.copy()
    peak_idx = np.argmax(original_h)
    h_remove[peak_idx-3:peak_idx+4] *= 0.5
    h_remove = normalize_and_clip(h_remove)
    c5 = compute_c5(h_remove)
    candidates.append({'h': h_remove.tolist(), 'c5_bound': c5, 'type': 'remove_peak'})
    
    return {'candidates': candidates, 'num_candidates': len(candidates)}