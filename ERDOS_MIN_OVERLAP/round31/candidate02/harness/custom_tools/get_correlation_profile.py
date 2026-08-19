def run(ctx, args):
    h_text = ctx.get_best_program()
    if not h_text or "h = " not in h_text:
        return {"error": "No h array found in program"}
    
    import re
    patterns = [
        r"h\s*=\s*array\s*\(([^)]+)\)",
        r"h\s*=\s*np\.array\s*\(([^)]+)\)"
    ]
    match = None
    for p in patterns:
        m = re.search(p, h_text, re.IGNORECASE)
        if m:
            match = m
            break
    
    if not match:
        return {"error": "Could not parse h array"}
    
    try:
        h_vals = [float(x.strip()) for x in match.group(1).split(",")]
        h_vals = np.array(h_vals)
    except:
        return {"error": "Failed to parse h values"}
    
    N = len(h_vals)
    domain = 2.0
    dx = domain / N
    h_padded = np.pad(h_vals, (0, N))
    j_padded = np.pad(1.0 - h_vals, (0, N))
    
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    overlap = correlation * dx
    
    top_k = np.argsort(overlap)[-3:][::-1]
    return {
        "problematic_k": [int(k) for k in top_k],
        "max_overlap": float(overlap.max()),
        "max_overlap_at_k": int(np.argmax(overlap)),
        "top_3_overlap": [float(overlap[k]) for k in top_k]
    }
