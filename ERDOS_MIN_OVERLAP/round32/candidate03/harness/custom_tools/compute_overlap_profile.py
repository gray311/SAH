def run(ctx, args):
    h = ctx.get_best_program()
    if h is None or h == "":
        return {"error": "No best program available"}
    
    # Extract h array - handle common patterns
    import re
    
    # Pattern 1: h = array([...])
    match = re.search(r"h\s*=\s*array\s*\(([^)]+)\)", h, re.IGNORECASE)
    if not match:
        # Pattern 2: h = np.array([...])
        match = re.search(r"np\.array\s*\(([^)]+)\)", h, re.IGNORECASE)
    
    if not match:
        return {"error": "Could not extract h array from program"}
    
    try:
        h_vals = [float(x.strip()) for x in match.group(1).split(",")]
        h_vals = np.array(h_vals)
    except:
        return {"error": "Failed to parse h values"}
    
    N = len(h_vals)
    if N != ctx.hypers.num_intervals:
        return {"error": f"Unexpected h length: {N} (expected {ctx.hypers.num_intervals})"}
    
    dx = 2.0 / N
    
    # Compute overlap profile
    h_padded = np.pad(h_vals, (0, N))
    j_padded = np.pad(1.0 - h_vals, (0, N))
    
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    overlap = correlation * dx
    
    # Find top 5 problematic k values
    top_k = np.argsort(overlap)[-5:][::-1]
    top_vals = overlap[top_k]
    
    return {
        "overlap_profile": [float(overlap[k]) for k in range(N)],
        "max_overlap": float(overlap.max()),
        "max_overlap_k": int(np.argmax(overlap)),
        "top_5_k": [int(k) for k in top_k],
        "top_5_overlap": [float(v) for v in top_vals]
    }
