def run(ctx, args):
    import math
    import numpy as np
    pattern = args.get("pattern", "boundary_mass")
    num_intervals = args.get("num_intervals", 50)
    dx = 2.0 / num_intervals
    
    h = np.zeros(num_intervals)
    
    if pattern == "single_block":
        # h=1 on [0,1], 0 on (1,2]
        end_idx = int(1.0 / dx)
        h[:end_idx] = 1.0
    
    elif pattern == "double_step":
        # h=0.5 on two intervals of width 0.5 each
        idx1 = int(0.0 / dx)
        idx2 = int(0.5 / dx)
        end1 = min(idx1 + int(0.5 / dx), num_intervals)
        end2 = min(idx2 + int(0.5 / dx), num_intervals)
        h[idx1:end1] = 0.5
        h[idx2:end2] = 0.5
    
    elif pattern == "boundary_mass":
        # h=1 on [0,0.5] ∪ [1.5, 2]
        idx1 = 0
        idx2 = int(1.5 / dx)
        end1 = min(int(0.5 / dx) + 1, num_intervals)
        end2 = num_intervals
        h[idx1:end1] = 1.0
        h[idx2:end2] = 1.0
    
    elif pattern == "three_interval":
        # Three consecutive intervals, each height 1/3
        start = int(0.0 / dx)
        width = int(1.0 / dx)
        end = min(start + width, num_intervals)
        h[start:end] = 1.0 / 3.0
    
    elif pattern == "shifted_block":
        # Try shifts around 0.25 to avoid self-overlap
        shifts = [0.0, 0.25, 0.5, 0.75, 1.0]
        best_shift = 0.0
        best_score = float('inf')
        
        # Use cheap probe if available
        if hasattr(ctx, 'probe'):
            for s in shifts:
                trial_h = np.zeros(num_intervals)
                idx_start = int(s / dx)
                end_idx = min(int((s+1) / dx) + 1, num_intervals)
                trial_h[idx_start:end_idx] = 1.0
                
                # Verify constraint
                integral = np.sum(trial_h) * dx
                if abs(integral - 1.0) < 0.01:
                    # Check C5 via approximation
                    j = 1.0 - trial_h
                    h_pad = np.pad(trial_h, (0, num_intervals))
                    j_pad = np.pad(j, (0, num_intervals))
                    corr = np.fft.ifft(np.fft.fft(h_pad) * np.conj(np.fft.fft(j_pad))).real
                    score = np.max(corr) * dx
                    if score < best_score:
                        best_score = score
                        best_shift = s
            h = np.zeros(num_intervals)
            idx_start = int(best_shift / dx)
            end_idx = min(int((best_shift+1) / dx) + 1, num_intervals)
            h[idx_start:end_idx] = 1.0
        else:
            # Default to shift 0.25
            idx_start = int(0.25 / dx)
            end_idx = min(int(1.25 / dx) + 1, num_intervals)
            h[idx_start:end_idx] = 1.0
    
    # Final constraint correction if needed
    integral = np.sum(h) * dx
    if abs(integral - 1.0) > 0.001:
        # Scale heights to satisfy integral constraint
        current_sum = np.sum(h)
        if current_sum > 0:
            scale = 1.0 / current_sum
            h = h * scale
        else:
            # Fallback: set first interval to make integral=1
            h = np.zeros(num_intervals)
            h[0] = 1.0 / dx
    
    # Clip to [0,1]
    h = np.clip(h, 0.0, 1.0)
    
    return {"h": h.tolist(), "pattern": pattern, "num_intervals": num_intervals,
            "integral": float(np.sum(h) * dx)}