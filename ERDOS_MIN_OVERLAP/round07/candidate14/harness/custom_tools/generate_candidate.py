def run(ctx, args):
    import numpy as np
    N = args.get('num_intervals', 800)
    x = np.linspace(0, 2, N+1)[:-1]
    dt = 2.0 / N
    h = np.zeros(N)
    c5 = 0.0
    
    ct = str(args.get('construction_type', 'single_step')).lower()
    
    if ct == 'single_step':
        # h=1 on [0,0.5], but we need integral=1, so scale
        h[:N//2] = 1.0
        integral = h.sum() * dt
        if integral > 0:
            h = h / integral
        
        # Compute c5 bound via FFT
        h_padded = np.pad(h, (0, N))
        corr = np.fft.ifft(np.fft.fft(h_padded) * np.fft.ifft(np.fft.fft(h_padded)).conj()).real
        c5 = np.max(corr) * dt
        
    elif ct == 'double_step':
        # Two equal peaks
        h[:N//4] = 0.5
        h[3*N//4:] = 0.5
        integral = h.sum() * dt
        if integral > 0:
            h = h / integral
        h_padded = np.pad(h, (0, N))
        corr = np.fft.ifft(np.fft.fft(h_padded) * np.fft.ifft(np.fft.fft(h_padded)).conj()).real
        c5 = np.max(corr) * dt
        
    elif ct == 'uniform_gap':
        # Uniform with a gap
        h[:N//3] = 1.0
        integral = h.sum() * dt
        if integral > 0:
            h = h / integral
        h_padded = np.pad(h, (0, N))
        corr = np.fft.ifft(np.fft.fft(h_padded) * np.fft.ifft(np.fft.fft(h_padded)).conj()).real
        c5 = np.max(corr) * dt
        
    elif ct == 'symmetric_triple':
        # Three equal symmetric peaks
        h[:N//6] = 1.0
        h[N//2-2*N//6:] = 1.0
        h[3*N//6:N//2+2*N//6] = 1.0
        integral = h.sum() * dt
        if integral > 0:
            h = h / integral
        h_padded = np.pad(h, (0, N))
        corr = np.fft.ifft(np.fft.fft(h_padded) * np.fft.ifft(np.fft.fft(h_padded)).conj()).real
        c5 = np.max(corr) * dt
        
    elif ct == 'concentrated':
        # Very concentrated mass
        h[:N//10] = 1.0
        integral = h.sum() * dt
        if integral > 0:
            h = h / integral
        h_padded = np.pad(h, (0, N))
        corr = np.fft.ifft(np.fft.fft(h_padded) * np.fft.ifft(np.fft.fft(h_padded)).conj()).real
        c5 = np.max(corr) * dt
    
    combined = {'construction': ct, 'N': N, 'h_values': h, 'integral': float(h.sum()*dt), 'c5_bound': float(c5)}
    return combined
