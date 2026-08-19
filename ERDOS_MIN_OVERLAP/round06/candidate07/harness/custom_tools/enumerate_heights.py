def run(ctx, args):
    import numpy as np
    from itertools import product
    N = args.get("num_intervals", 5)
    heights = args.get("heights", [0.0, 0.5, 1.0])
    dx = 2.0 / N
    best = []
    for assign in product(heights, repeat=N):
        h = np.array(assign)
        integral = h.sum() * dx
        if 0.99 <= integral <= 1.01:
            best.append({"h": h.tolist(), "integral": float(integral), "score": 1.0})
        if h.sum() > 0:
            s = h / h.sum()
            integral = s.sum() * dx
            if 0.99 <= integral <= 1.01:
                best.append({"h": s.tolist(), "integral": float(integral), "score": 1.0})
    best.sort(key=lambda x: x["integral"], reverse=True)
    return {"candidates": best[:10], "total": len(best)}
