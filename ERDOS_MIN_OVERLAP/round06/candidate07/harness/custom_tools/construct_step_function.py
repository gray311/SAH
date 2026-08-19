def run(ctx, args):
    import numpy as np
    N = args.get("num_intervals", 100)
    dx = 2.0 / N
    h = np.zeros(N)
    pattern = args.get("pattern", "single")
    config = args.get("config", {})
    if pattern == "single":
        h[:int(1/dx)] = 1.0
    elif pattern == "bimodal":
        a = config.get("a", 0.25)
        for i in range(N):
            x = (i + 0.5) * dx
            if (x >= a and x <= 1-a) or (x >= 1+a and x <= 2-(1-a)):
                h[i] = 1.0
    elif pattern == "tri":
        h1 = config.get("h1", 1.0)
        h2 = config.get("h2", 0.5)
        h3 = config.get("h3", 0.0)
        iv = N // 3
        h[:iv] = h1
        h[iv:2*iv] = h2
        h[2*iv:] = h3
    elif pattern == "random":
        h = np.random.choice([0.0, 0.5, 1.0], N, p=[0.3, 0.4, 0.3])
    h = np.clip(h, 0.0, 1.0)
    return {"h": h.tolist(), "integral": float(h.sum() * dx), "pattern": pattern}
