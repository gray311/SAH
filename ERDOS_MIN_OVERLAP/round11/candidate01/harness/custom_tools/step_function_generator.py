def run(ctx, args):
    import numpy as np
    N = args.get("N", 800)
    k = args.get("k", 500)
    H_low = args.get("H_low", 0.0)
    domain = 2.0
    dx = domain / N
    
    # Compute H_high to satisfy integral(h) = 1
    # integral = H_high * k * dx + H_low * (N-k) * dx = 1
    # H_high = (1 - H_low*(N-k)*dx) / (k*dx) = (1 - H_low*(N-k)) / k
    H_high = (1.0 - H_low * (N - k)) / k
    
    # Validate H_high is in [0, 1]
    if H_high < 0 or H_high > 1:
        return {"error": "H_high out of [0,1] for k=" + str(k) + ", H_low=" + str(H_low) + ", valid: False"}
    
    # Create step function: first k intervals at H_high, last at H_low
    h = np.full(N, H_low)
    h[:k] = H_high
    
    # Return discretization and parameters for EVOLVE-BLOCK editing
    return {
        "h": h,
        "H_high": float(H_high),
        "H_low": float(H_low),
        "k": k,
        "N": N,
        "dx": float(dx),
        "valid": True,
        "integral_check": float(h.sum() * dx)
    }
