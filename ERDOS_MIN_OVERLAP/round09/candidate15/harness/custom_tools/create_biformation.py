def run(ctx, args):
    import numpy as np
    N = 800
    x = np.linspace(0, 2, N)
    
    # Base: large negative value
    latent = -20.0 * np.ones(N)
    
    # Peak at 0.25: width parameter 0.05, amplitude 15
    peak1 = 15.0 * np.exp(-((x - 0.25) / 0.05)**2 * 50)
    
    # Peak at 0.75: symmetric
    peak2 = 15.0 * np.exp(-((x - 0.75) / 0.05)**2 * 50)
    
    latent = peak1 + peak2
    
    return {"latent": latent}
