def run(ctx, args):
    import re
    import numpy as np
    h = ctx.get_best_program()
    if not h:
        return {"error": "No program"}
    # Simple extraction
    try:
        # Look for h = array([...])
        m = re.search(r'h\s*=\s*(array|np\.array)\s*\(([^)]+)\)', h, re.IGNORECASE)
        if not m:
            return {"error": "Could not find h array"}
        h_vals = np.array([float(x.strip()) for x in m.group(2).split(',')])
        N = len(h_vals)
        dx = 2.0 / N
        h_p = np.pad(h_vals, (0, N))
        j_p = np.pad(1.0 - h_vals, (0, N))
        corr = np.fft.ifft(np.fft.fft(h_p) * np.conj(np.fft.fft(j_p))).real
        overlap = corr * dx
        top_idx = np.argsort(overlap)[-3:][::-1]
        return {"top_k": [int(i) for i in top_idx], "overlap": [float(overlap[i]) for i in top_idx]}
    except:
        return {"error": "Analysis failed", "note": "fallback to random mutations"}
