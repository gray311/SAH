def run(ctx, args):
    import numpy as np
    N = 800
    pattern = args.get("pattern_type", "bimodal")
    h = np.zeros(N)
    n1, n0_5 = 200, 400
    if pattern == "bimodal":
        h[:n1] = 1.0
        h[-n1:] = 1.0
        h[n1:-n1] = 0.5
    elif pattern == "golomb":
        for pos in [0, 0.25, 0.625, 0.9375, 1.0]:
            start = int(pos * N)
            end = start + 40
            h[start:end] = 1.0
        h[h == 0] = 0.5
    elif pattern == "alternating":
        for i in range(N // 4):
            h[i*4:i*4+2] = 1.0
            h[i*4+2:i*4+4] = 0.5
    elif pattern == "concentrated":
        h[:150] = 1.0
        h[150:550] = 0.5
        h[550:] = 1.0
    return {"h": h.tolist(), "sum_check": float(np.sum(h))}
