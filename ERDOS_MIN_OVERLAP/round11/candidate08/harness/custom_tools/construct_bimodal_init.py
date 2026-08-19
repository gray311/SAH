def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    x = np.linspace(0, domain, N)
    peak_width = args.get("peak_width", 0.15)
    peak_height = args.get("peak_height", 10.0)
    a1, a2 = 0.25, 0.75
    peak1 = np.exp(-((x - a1) / peak_width)**2 * 20)
    peak2 = np.exp(-((x - a2) / peak_width)**2 * 20)
    latent = (peak1 + peak2) * peak_height
    h = 1.0 / (1.0 + np.exp(-latent))
    integral_h = np.sum(h) * dx
    if integral_h != 1.0:
        scale = 1.0 / integral_h
        h_scaled = h * scale
        eps = 1e-10
        h_clipped = np.clip(h_scaled, eps, 1-eps)
        latent = np.log(h_clipped / (1 - h_clipped))
    else:
        latent = np.log(h / (1 - h))
    return {"latent": latent.tolist(), "peak_width_used": peak_width,
            "peak_height_used": peak_height, "integral_h": float(np.sum(1/(1+np.exp(-latent))) * dx)}
