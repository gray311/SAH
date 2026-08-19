def run(ctx, args):
    import re
    import numpy as np
    
    h = ctx.get_best_program()
    if not h or h.strip() == "":
        return {"error": "No h array found"}
    
    # Extract h array
    match = re.search(r'h\s*=\s*array\s*\(([^)]+)\)', h)
    if not match:
        return {"error": "Could not parse h array"}
    
    try:
        h_vals = [float(x.strip()) for x in match.group(1).split(',')]
        h_vals = np.array(h_vals)
    except:
        return {"error": "Failed to parse h values"}
    
    N = len(h_vals)
    domain = 2.0
    dx = domain / N
    
    # Compute current overlap structure
    h_padded = np.pad(h_vals, (0, N))
    j_padded = np.pad(1.0 - h_vals, (0, N))
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    overlap = correlation * dx
    
    target_shifts = args.get("target_shifts", [])
    mutation_type = args.get("mutation_type", "narrow_peak")
    intensity = args.get("intensity", 0.3)
    width = args.get("width", 0.1)
    
    edits = []
    new_h_vals = h_vals.copy()
    
    for k in target_shifts:
        k_int = int(round(float(k)))
        if k_int < 0 or k_int >= N:
            continue
        
        overlap_k = overlap[k_int]
        if overlap_k <= 0:
            continue
        
        mutation_type = mutation_type if mutation_type else "narrow_peak"
        
        if mutation_type == "narrow_peak":
            # Reduce h values in a narrow window around the problematic k
            i = k_int
            if 0 <= i < N:
                half_w = max(1, int(width * N / 2))
                if i - half_w >= 0 and i + half_w < N:
                    center_val = h_vals[i]
                    new_vals = h_vals.copy()
                    for j in range(i-half_w, i+half_w+1):
                        new_vals[j] = center_val * (1 - intensity * 0.3)
                    
                    # Clip to [0,1]
                    new_vals = np.clip(new_vals, 0, 1)
                    
                    # Renormalize to preserve integral
                    total = np.sum(new_vals) * dx
                    if total > 0 and total != 1.0:
                        scale = 1.0 / total
                        new_vals = new_vals * scale
                    
                    new_h_vals = new_vals
    
    # Build new h array string
    h_new = ", ".join([str(round(float(v), 6)) for v in new_h_vals])
    
    return {"edits": [{"action": "edit_h_array", "new_h": h_new}]}
