def run(ctx, args):
    import numpy as np
    h = np.array(ctx.get_program().split('\n')[100:200])  # Extract h array from program
    if len(h) == 0:
        return {"note": "Could not extract h from program", "variants": []}
    
    dx = 2.0 / len(h)
    variants = []
    best_c5 = None
    
    strategy = args.get("strategy", "shift_peak")
    magnitude = args.get("magnitude", 0.2)
    num_variants = args.get("num_variants", 5)
    
    for i in range(num_variants):
        if strategy == "shift_peak":
            # Shift peaks left or right
            shift = np.random.choice([-1, 1]) * (dx * magnitude)
            new_h = h.copy()
            new_h = np.roll(new_h, int(shift / dx))
            new_h = new_h / (np.sum(new_h) * dx)
            new_h = np.clip(new_h, 0.001, 1.0)
            new_h = new_h / (np.sum(new_h) * dx)
            new_h[0] = 1.0 / len(new_h)  # Normalize
            h_new = new_h
            
        elif strategy == "split_peak":
            # Split largest peak into two
            new_h = h.copy()
            max_idx = np.argmax(new_h)
            split_idx = max_idx + int(dx * magnitude * len(h))
            if split_idx <= len(new_h) - 1:
                # Move mass from max to split point
                delta = 0.5 * new_h[max_idx]
                new_h[max_idx] -= delta
                new_h[split_idx] += delta
                new_h = new_h / (np.sum(new_h) * dx)
            else:
                new_h = new_h / (np.sum(new_h) * dx)
            h_new = new_h
            
        elif strategy == "adjust_threshold":
            # Adjust threshold in bipartite-like pattern
            new_h = h.copy()
            threshold_idx = np.argmin(new_h)
            shift_idx = int(dx * magnitude * len(h))
            if threshold_idx + shift_idx < len(new_h):
                delta = 0.1 * magnitude
                new_h[threshold_idx:threshold_idx+shift_idx] -= delta
                new_h[threshold_idx+shift_idx:] += delta
                new_h = new_h / (np.sum(new_h) * dx)
            else:
                new_h = new_h / (np.sum(new_h) * dx)
            h_new = new_h
            
        # Normalize and clip
        h_new = h_new / (np.sum(h_new) * dx)
        h_new = np.clip(h_new, 0.001, 1.0)
        h_new = h_new / (np.sum(h_new) * dx)
        
        # Compute c5 bound
        h_padded = np.pad(h_new, (0, len(h_new)))
        j_padded = np.pad(1.0 - h_new, (0, len(h_new)))
        corr = np.fft.ifft(np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))).real
        c5_bound = np.max(corr * dx)
        
        variants.append({
            "h": h_new.tolist(),
            "c5_bound": float(c5_bound),
            "strategy_applied": strategy
        })
    
    return {"variants": variants, "num_variants": len(variants)}
