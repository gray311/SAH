def run(ctx, args):
    import re
    import numpy as np
    h = ctx.get_best_program()
    if h is None or h == "":
        return {"error": "No best program available"}
    
    # Try to extract h array - look for different patterns
    patterns = [
        r"'h\s*=\s*array\s*\(([^)]+)",
        r'h\s*=\s*array\s*\(([^)]+)',
        r'h\s*=\s*np\.array\s*\(([^)]+)'
    ]
    
    match = None
    for pattern in patterns:
        m = re.search(pattern, h, re.IGNORECASE)
        if m:
            match = m
            break
    
    if not match:
        return {"error": "Could not parse h array. Tried patterns: " + str(patterns)}
    
    try:
        h_vals = [float(x.strip()) for x in match.group(1).split(",")]
        h_vals = np.array(h_vals)
    except Exception as e:
        return {"error": "Failed to parse h values: " + str(e)}
    
    N = len(h_vals)
    domain = 2.0
    dx = domain / N
    
    h_padded = np.pad(h_vals, (0, N))
    j_padded = np.pad(1.0 - h_vals, (0, N))
    
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    
    overlap_values = correlation * dx
    top_k_indices = np.argsort(overlap_values)[-5:][::-1]
    top_k_values = top_k_indices.astype(np.int32)
    top_overlap_values = overlap_values[top_k_indices]
    
    return {
        "top_problematic_k": [int(k) for k in top_k_values],
        "top_overlap_values": [float(v) for v in top_overlap_values],
        "max_overlap": float(overlap_values.max()),
        "max_overlap_at_k": int(np.argmax(overlap_values))
    }