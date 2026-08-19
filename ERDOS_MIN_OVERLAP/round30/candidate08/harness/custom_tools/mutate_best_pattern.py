def run(ctx, args):
    import numpy as np
    
    # Get best pattern from previous search_patterns call
    best_pattern = None
    best_c5 = float('inf')
    
    candidates = ctx.scratch_read('search_patterns_output')
    if candidates and 'candidates' in candidates:
        for cand in candidates['candidates']:
            if cand['c5_bound'] < best_c5:
                best_c5 = cand['c5_bound']
                best_pattern = cand['h']
    
    if best_pattern is None:
        return {"error": "No pattern found in scratch space", "candidates": []}
    
    N = 800
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
    
    def mutate_pattern(h, mutation_type, mag):
        """Apply a single mutation and return mutated array."""
        h_mut = h.copy()
        
        if mutation_type == 'width':
            # Find peaks and adjust widths
            peaks = np.where(h > 0.5)[0]
            for peak_idx in peaks[:3]:  # Top 3 peaks
                if len(peaks) > 1:
                    peak_val = peaks[np.argmin(np.abs(peaks - peak_idx))]
                    width_change = int(mag * N)
                    half_w = len(h) // len(peaks)
                    start = max(0, peak_idx - half_w + width_change)
                    end = min(N, peak_idx + half_w + width_change)
                    h_mut[start:end] = h[start:end] * (1 + 0.1 * np.random.randn())
        
        elif mutation_type == 'shift':
            # Shift all peaks by mag units
            x = np.linspace(0, 2, N)
            for peak_idx in np.where(h > 0.5)[0][:3]:
                shift_idx = int(mag / dx)
                new_peak = peak_idx + shift_idx
                if 0 < new_peak < N:
                    h_mut = h_mut + (h[new_peak] - h[peak_idx])
                    h_mut[peak_idx] = h[peak_idx]
                    h_mut[new_peak] = h[new_peak]
        
        elif mutation_type == 'amplitude':
            # Adjust amplitudes of peaks
            peaks = np.where(h > 0.5)[0]
            for peak_idx in peaks[:3]:
                amp_change = 0.2 * np.random.randn()
                h_mut[peak_idx] = np.clip(h_mut[peak_idx] + amp_change, 0.001, 1.0)
        
        return normalize_and_clip(h_mut)
    
    # Apply 3 different mutations
    variants = []
    mutation_types = ['width', 'shift', 'amplitude']
    for i, mut_type in enumerate(mutation_types):
        h_mut = mutate_pattern(best_pattern, mut_type, args.get('mutation_magnitude', 0.1))
        c5_bound = compute_c5(h_mut)
        variants.append({
            'h': h_mut.tolist(),
            'c5_bound': float(c5_bound),
            'mutation_type': mutation_types[i],
            'pattern_type': 'mutated'
        })
    
    return {"candidates": variants, "num_candidates": 3}
