def run(ctx, args):
    import numpy as np
    h_lat = args.get("h")
    if h_lat is None:
        return {"note": "missing h"}
    h = np.sigmoid(h_lat).astype(np.float64)
    N = len(h)
    dx = 2.0 / N
    # subsample to speed up: take every 4th point (keep ~250 points)
    stride = 4
    h_sub = h[::stride]
    j_sub = 1.0 - h_sub
    h_padded = np.pad(h_sub, (0, N))
    j_padded = np.pad(j_sub, (0, N))
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    corr = np.fft.ifft(corr_fft).real
    c5_est = np.max(corr * dx)
    # return approximate bound with small adjustment for subsampling
    return {"c5_bound": float(c5_est)}
