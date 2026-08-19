def run(ctx, args):
    import numpy as np
    N = 800
    dx = 2.0 / N
    
    bipartite_h = np.zeros(N)
    bipartite_h[int(0.5*N):int(1.0*N)] = 2.0
    corr = np.fft.ifft(np.fft.fft(np.pad(bipartite_h, (0,N))) * np.conj(np.fft.fft(np.pad(1.0-bipartite_h, (0,N))))).real
    bipartite_c5 = np.max(corr * dx)
    
    two_block_h = np.zeros(N)
    two_block_h[:int(0.5*N)] = 1.0
    two_block_h[int(1.0*N):int(1.5*N)] = 1.0
    corr = np.fft.ifft(np.fft.fft(np.pad(two_block_h, (0,N))) * np.conj(np.fft.fft(np.pad(1.0-two_block_h, (0,N))))).real
    two_block_c5 = np.max(corr * dx)
    
    tri_h = np.zeros(N)
    tri_h[int(0.4*N):int(0.8*N)] = 2.5
    corr = np.fft.ifft(np.fft.fft(np.pad(tri_h, (0,N))) * np.conj(np.fft.fft(np.pad(1.0-tri_h, (0,N))))).real
    tri_c5 = np.max(corr * dx)
    
    return {
        "candidates": [
            {"name": "bipartite_step", "h": bipartite_h.tolist(), "c5_bound": float(bipartite_c5)},
            {"name": "two_block", "h": two_block_h.tolist(), "c5_bound": float(two_block_c5)},
            {"name": "tri_step", "h": tri_h.tolist(), "c5_bound": float(tri_c5)}
        ]
    }
