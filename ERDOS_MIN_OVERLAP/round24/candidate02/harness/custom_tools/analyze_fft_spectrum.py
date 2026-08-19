def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    try:
        raw_h = ctx.get_program().split('h_values = [')[1].split(']')[0]
        h = np.array([float(x.strip()) for x in raw_h.strip().split(',')])
    except (IndexError, ValueError):
        h = np.ones(N) * 0.5
    
    h = np.clip(h, 0.001, 0.999)
    
    j = 1.0 - h
    h_padded = np.pad(h, (0, N))
    j_padded = np.pad(j, (0, N))
    
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    
    c5_bound = np.max(correlation * dx)
    
    # Find peaks in h
    h_smoother = np.convolve(h, np.ones(5)/5, mode='same')
    if len(h_smoother) > 0:
        peak_indices = np.where(h_smoother > h_smoother[0] * 2.0)[0]
        peak_locations = [float(i * dx) for i in peak_indices[:5]] if len(peak_indices) > 0 else []
    else:
        peak_locations = []
    
    # Energy spectrum
    energy_spectrum = np.abs(np.fft.fft(h))[:N//4]
    
    # Find max overlap
    if len(correlation) > 2:
        max_k = np.argmax(correlation[1:-1])
        max_overlap_index = float(max_k * dx)
    else:
        max_overlap_index = 0.0
    
    # Qualitative pattern
    if len(peak_locations) >= 3:
        overlap_pattern = "multi-peak with potential inter-peak overlap"
    elif len(peak_locations) >= 2:
        overlap_pattern = "bipartite-like with possible edge effects"
    else:
        overlap_pattern = "unimodal (high overlap likely)"
    
    return {
        "c5_bound": float(c5_bound),
        "peak_locations": peak_locations,
        "energy_spectrum": energy_spectrum.tolist(),
        "max_overlap_index": max_overlap_index,
        "overlap_pattern": overlap_pattern,
        "note": "Use peak_locations to guide edits; consider splitting peaks or adding intermediate peaks"
    }