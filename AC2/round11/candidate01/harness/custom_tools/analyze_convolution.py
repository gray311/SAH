def run(ctx, args):
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"error": "no evolve block"}
    
    try:
        import re
        import numpy as np
        
        n = 450
        f = np.zeros(n)
        f[int(0.20*n):int(0.30*n)] = 1.4
        f[int(0.30*n):int(0.50*n)] = 1.9
        f[int(0.50*n):int(0.70*n)] = 2.1
        f[int(0.70*n):int(0.85*n)] = 1.5
        f[int(0.85*n):int(1.0*n)] = 0.8
        
        f_non_negative = np.maximum(f, 0)
        N = n
        padded_f = np.pad(f_non_negative, (0, N))
        fft_f = np.fft.fft(padded_f)
        convolution = np.fft.ifft(fft_f * fft_f).real
        
        h = 1.0 / (len(convolution) + 1)
        l2_norm_squared = np.sum((h / 3) * (convolution[:-1]**2 + convolution[:-1]*convolution[1:] + convolution[1:]**2))
        norm_1 = np.sum(np.abs(convolution)) / (len(convolution) + 1)
        norm_inf = np.max(np.abs(convolution))
        c2_ratio = l2_norm_squared / (norm_1 * norm_inf)
        
        peak_idx = np.argmax(np.abs(convolution))
        peak_value = np.abs(convolution)[peak_idx]
        peak_fraction = peak_value / (np.sum(np.abs(convolution)))
        l2_concentration = l2_norm_squared / (peak_value ** 2)
        
        peak_fraction_float = float(peak_fraction)
        
        return {
            "l2_norm_squared": float(l2_norm_squared),
            "norm_1": float(norm_1),
            "norm_inf": float(norm_inf),
            "c2_ratio": float(c2_ratio),
            "peak_idx": int(peak_idx),
            "peak_fraction": peak_fraction_float,
            "l2_concentration": float(l2_concentration),
            "peak_idx_fraction": float(peak_idx / n),
            "insights": [
                f"Peak occurs at {peak_idx/n:.2f} (fraction of domain)",
                f"Peak accounts for {peak_fraction_float*100:.1f}% of L1 norm",
                f"L2 energy concentration: {l2_concentration:.2f}",
                "Recommendation: If peak_fraction > 0.2, try widening or adding side peaks."
            ]
        }
    except Exception as e:
        return {"error": str(e)}