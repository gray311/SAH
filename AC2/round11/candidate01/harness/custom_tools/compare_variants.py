def run(ctx, args):
    variants = args.get("variants", [])
    n = 512
    
    if not variants:
        return {"error": "no variants provided"}
    
    results = []
    for v in variants:
        name = v.get("name", "unknown")
        config = v.get("config", {})
        
        import numpy as np
        
        f = np.ones(n)
        if "heights" in config:
            heights = config["heights"]
            if len(heights) >= 3:
                f = f[int(0.2*n):int(0.3*n)] = heights[0]
                f = f[int(0.3*n):int(0.5*n)] = heights[1]
                f = f[int(0.5*n):int(0.7*n)] = heights[2]
        
        f_nn = np.maximum(f, 0)
        padded = np.pad(f_nn, (0, n))
        fft_f = np.fft.fft(padded)
        conv = np.fft.ifft(fft_f * fft_f).real
        
        h = 1.0 / (n + 1)
        l2_sq = np.sum((h / 3) * (conv[:-1]**2 + conv[:-1]*conv[1:] + conv[1:]**2))
        l1 = np.sum(np.abs(conv)) / (n + 1)
        l_inf = np.max(np.abs(conv))
        
        c2_heuristic = l2_sq / (l1 * l_inf)
        
        results.append({
            "variant": name,
            "c2_heuristic": float(c2_heuristic),
            "l2_sq": float(l2_sq),
            "l1": float(l1),
            "l_inf": float(l_inf)
        })
    
    results.sort(key=lambda x: x["c2_heuristic"], reverse=True)
    
    return {
        "ranking": results,
        "top_recommendation": results[0]["variant"] if results else None
    }