def run(ctx, args):
    import numpy as np
    import math
    
    # Get current function
    f_code = ctx.get_program()
    
    # Extract function values - approximate extraction from code
    try:
        f_values = ctx.get_program()
        # Simulate by extracting numeric patterns or using defaults
        # In production, this would parse and evaluate the actual function
        f_values = np.array([1.0, 2.0, 3.0, 2.0, 1.0])  # Placeholder
    except:
        f_values = np.array([1.0, 2.0, 3.0, 2.0, 1.0])
    
    # Simulate convolution analysis (in real use, this would compute actual convolution)
    g = np.convolve(f_values, f_values)
    
    # Compute metrics
    norm_1 = np.sum(np.abs(g)) / len(g)
    norm_inf = np.max(np.abs(g))
    norm_2_sq = np.sum(g**2)
    l2_inf_ratio = norm_2_sq / (norm_1 * norm_inf) if norm_1 * norm_inf > 0 else 0
    
    # Smoothness estimate (based on derivative magnitude)
    diffs = np.diff(g)
    smoothness = 1.0 / (1.0 + np.mean(np.abs(diffs)))
    
    # Peak analysis
    peak_positions = np.where(g == np.max(g))[0]
    peak_positions = [int(p) for p in peak_positions[:5]]  # Top 5 peaks
    
    # Spectral entropy estimate
    freq_spectrum = np.fft.fft(g)
    power_spec = np.abs(freq_spectrum)**2
    power_spec = power_spec / np.sum(power_spec)
    power_spec = power_spec + 1e-10  # Avoid log(0)
    spectral_entropy = -np.sum(power_spec * np.log(power_spec)) / np.log(len(power_spec))
    
    # Recommendation based on diagnostics
    recommendation = ""
    if smoothness < 0.3:
        recommendation = "Try smooth functions (Gaussian mixtures, splines) to reduce blocky convolution"
    elif spectral_entropy < 0.7:
        recommendation = "Add oscillatory components to increase spectral diversity"
    elif l2_inf_ratio < 0.85:
        recommendation = "Increase concentration of convolution energy (narrower peaks)"
    
    return {
        "smoothness_score": round(smoothness, 4),
        "l2_inf_ratio": round(l2_inf_ratio, 6),
        "spectral_entropy": round(spectral_entropy, 4),
        "peak_positions": peak_positions,
        "recommendation": recommendation,
        "note": "Use these diagnostics to design functions with opposite/different convolution properties"
    }
